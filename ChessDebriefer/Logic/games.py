import io
import chess.pgn
import chess.engine
from ChessDebriefer.models import Openings, FieldsCache


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


def find_opening(game):
    if not game.eco or str(game.opening_id) == "000000000000000000000000":
        openings = Openings.objects
        cached_fields = FieldsCache.objects.first()
        fields = ["eco", "opening_id"]
        filtered_openings = list(filter(lambda op: game.moves.startswith(op.moves), openings))
        opening = filtered_openings[0]
        for opn in filtered_openings:
            split1 = opn.moves.split(" ")
            split2 = opening.moves.split(" ")
            if len(split1) > len(split2):
                opening = opn
        setattr(game, "eco", opening.eco)
        setattr(game, "opening_id", opening.id)
        game.save()
        for field in fields:
            if getattr(game, field) not in getattr(cached_fields, field):
                temp = getattr(cached_fields, field)
                temp.append(getattr(game, field))
                setattr(cached_fields, field, temp)
                cached_fields.save()


# TODO opening evaluation
