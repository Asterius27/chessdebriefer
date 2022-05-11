import io
import chess.pgn
import chess.engine
import chess.polyglot
from ChessDebriefer.models import Openings


# evaluation isn't perfect, more time you give it the better the result. Results are more precise in middle game
# only evaluates in centipawns, positive means an advantage for white, negative means an advantage for black
# slow
def evaluate_game(game):
    pgn = io.StringIO(game.moves)
    parsed_game = chess.pgn.read_game(pgn)
    engine = chess.engine.SimpleEngine.popen_uci(r"/code/stockfish_14_x64_avx2")  # stockfish_14.1_win_x64_avx2.exe
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
        if idd != "" and eco != "":
            setattr(game, "eco", eco)
            setattr(game, "opening_id", idd)


# slow
def evaluate_opening_engine(opening):
    if not opening.engine_evaluation:
        pgn = io.StringIO(opening.moves)
        parsed_game = chess.pgn.read_game(pgn)
        engine = chess.engine.SimpleEngine.popen_uci(r"/code/stockfish_14_x64_avx2")  # stockfish_14.1_win_x64_avx2.exe
        info = engine.analyse(parsed_game.end().board(), chess.engine.Limit(time=1))
        t = str(info["score"].pov(True))
        if t.startswith("#"):
            setattr(opening, "engine_evaluation", t)
        else:
            setattr(opening, "engine_evaluation", str(round(int(t) / 100., 2)))
        engine.quit()
        opening.save()
