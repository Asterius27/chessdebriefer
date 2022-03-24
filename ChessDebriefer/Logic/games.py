import io
import chess.pgn
import chess.engine
import chess.polyglot
from bson import ObjectId
from mongoengine import Q
from ChessDebriefer.models import Openings, FieldsCache, Games


# TODO do something to make it quicker, maybe background processing of matches?
# evaluation isn't perfect, more time you give it the better the result. Results are more precise in middle game
# only evaluates in centipawns, positive means an advantage for white, negative means an advantage for black
# slow
def evaluate_game(game):
    pgn = io.StringIO(game.moves)
    parsed_game = chess.pgn.read_game(pgn)
    engine = chess.engine.SimpleEngine.popen_uci("stockfish_14.1_win_x64_avx2.exe")
    best_moves = []
    moves_evaluation = []
    while not parsed_game.is_end():
        node = parsed_game.variations[0]
        result = engine.analysis(parsed_game.board(), chess.engine.Limit(time=1))
        info = engine.analyse(parsed_game.board(), chess.engine.Limit(time=1))
        t = str(info["score"].pov(True))
        best_moves.append(parsed_game.board().san(result.wait().move))
        if t.startswith("#"):
            moves_evaluation.append(t)
        else:
            moves_evaluation.append(str(round(int(t) / 100., 2)))
        parsed_game = node
    engine.quit()
    setattr(game, "best_moves", best_moves)
    setattr(game, "moves_evaluation", moves_evaluation)
    game.save()


def average_game_centipawn(game, name):
    i = 0
    moves = 0
    centipawn = 0.
    if not game.moves_evaluation:
        evaluate_game(game)
    if game.white == name:
        for evaluation in game.moves_evaluation:
            if i % 2 == 0:
                if not evaluation.startswith("#"):
                    centipawn = centipawn + float(evaluation)
                    moves = moves + 1
            i = i + 1
    if game.black == name:
        for evaluation in game.moves_evaluation:
            if i % 2 != 0:
                if not evaluation.startswith("#"):
                    centipawn = centipawn + (float(evaluation) * -1)
                    moves = moves + 1
            i = i + 1
    return round(centipawn / moves, 2)


# pretty slow
def find_opening(game, update=False):
    if not game.eco or str(game.opening_id) == "000000000000000000000000" or update:
        openings = Openings.objects.aggregate([
            {
                '$addFields': {'searchIndex': {'$indexOfCP': [game.moves, '$moves']}}
            },
            {
                '$match': {'searchIndex': {'$ne': -1}}
            },
            {
                '$project': {
                    '_id': 1,
                    'eco': 1,
                    'moves': 1,
                    'moves_length': {'$strLenCP': '$moves'}
                }
            },
            {
                '$sort': {'moves_length': 1}
            }
        ])
        eco = ""
        idd = ""
        for opening in openings:
            if game.moves.startswith(opening['moves']):
                eco = opening['eco']
                idd = opening['_id']
        """
        openings = Openings.objects
        filtered_openings = list(filter(lambda op: game.moves.startswith(op.moves), openings))
        opening = filtered_openings[0]
        for opn in filtered_openings:
            split1 = opn.moves.split(" ")
            split2 = opening.moves.split(" ")
            if len(split1) > len(split2):
                opening = opn
        """
        cached_fields = FieldsCache.objects.first()
        fields = ["eco", "opening_id"]
        setattr(game, "eco", eco)
        setattr(game, "opening_id", idd)
        game.save()
        for field in fields:
            if getattr(game, field) not in getattr(cached_fields, field):
                temp = getattr(cached_fields, field)
                temp.append(getattr(game, field))
                setattr(cached_fields, field, temp)
                cached_fields.save()


# slow
def evaluate_opening_engine(opening):
    if not opening.engine_evaluation:
        pgn = io.StringIO(opening.moves)
        parsed_game = chess.pgn.read_game(pgn)
        engine = chess.engine.SimpleEngine.popen_uci("stockfish_14.1_win_x64_avx2.exe")
        info = engine.analyse(parsed_game.end().board(), chess.engine.Limit(time=1))
        t = str(info["score"].pov(True))
        if t.startswith("#"):
            setattr(opening, "engine_evaluation", t)
        else:
            setattr(opening, "engine_evaluation", str(round(int(t) / 100., 2)))
        engine.quit()
        opening.save()


# slow
def evaluate_opening_database(opening, min_elo, tournament):
    cached_fields = FieldsCache.objects.first()
    filtered_games = Games.objects.filter((Q(eco="") | Q(opening_id=ObjectId("000000000000000000000000")))
                                          & Q(moves__startswith=opening.moves))
    filtered_openings = Openings.objects.filter(Q(id__ne=opening.id) & Q(moves__startswith=opening.moves))
    filtered_games_final = []
    for g in filtered_games:
        flag = False
        for op in filtered_openings:
            if g.moves.startswith(op.moves):
                flag = True
        if not flag:
            filtered_games_final.append(g)
    for gm in filtered_games_final:
        setattr(gm, "eco", opening.eco)
        setattr(gm, "opening_id", opening.id)
        gm.save()
    if getattr(opening, "eco") not in getattr(cached_fields, "eco"):
        temp = getattr(cached_fields, "eco")
        temp.append(getattr(opening, "eco"))
        setattr(cached_fields, "eco", temp)
        cached_fields.save()
    if getattr(opening, "id") not in getattr(cached_fields, "opening_id"):
        temp = getattr(cached_fields, "opening_id")
        temp.append(getattr(opening, "id"))
        setattr(cached_fields, "opening_id", temp)
        cached_fields.save()
    if tournament == "true":
        games = Games.objects.filter(Q(opening_id=opening.id) & Q(event__contains="tournament") &
                                     Q(white_elo__gte=min_elo) & Q(black_elo__gte=min_elo))
    else:
        games = Games.objects.filter(Q(opening_id=opening.id) & Q(white_elo__gte=min_elo) & Q(black_elo__gte=min_elo))
    white_wins = 0
    black_wins = 0
    draws = 0
    percentage_white_wins = 0.
    percentage_black_wins = 0.
    percentage_draws = 0.
    for game in games:
        if game.result == "1-0":
            white_wins = white_wins + 1
        if game.result == "0-1":
            black_wins = black_wins + 1
        if game.result == "1/2-1/2":
            draws = draws + 1
    if white_wins + black_wins + draws != 0:
        percentage_white_wins = round((white_wins / (white_wins + black_wins + draws)) * 100, 2)
        percentage_black_wins = round((black_wins / (white_wins + black_wins + draws)) * 100, 2)
        percentage_draws = round((draws / (white_wins + black_wins + draws)) * 100, 2)
    return {"white_wins": white_wins, "black_wins": black_wins, "draws": draws,
            "percentage_white_wins": percentage_white_wins, "percentage_black_wins": percentage_black_wins,
            "percentage_draws_wins": percentage_draws}


# find good book? how to use it to evaluate boards?
def polyglot(game):
    pgn = io.StringIO(game.moves)
    parsed_game = chess.pgn.read_game(pgn)
    with chess.polyglot.open_reader("polyglot/performance.bin") as reader:
        for entry in reader.find_all(parsed_game.end().board()):
            print(entry.move, entry.weight, entry.learn)
    print("-------------------------------")
