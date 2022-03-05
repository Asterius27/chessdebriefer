import datetime
import io
import os
import chess.pgn
import chess.engine
from mongoengine import Q
from ChessDebriefer.models import Games


# only works with 1 file upload at a time, and it takes a lot of time to parse everything
def handle_pgn_uploads(f):
    with open('temp.pgn', 'wb+') as temp:
        for chunk in f.chunks():
            temp.write(chunk)
    with open('temp.pgn') as pgn:
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break
            arr = game.headers["UTCDate"].split(".")
            date = datetime.datetime(int(arr[0]), int(arr[1]), int(arr[2]))
            if game.headers["Black"] != "?" and game.headers["White"] != "?":
                Games(event=game.headers["Event"], site=game.headers["Site"], white=game.headers["White"],
                      black=game.headers["Black"], result=game.headers["Result"], date=date,
                      white_elo=game.headers["WhiteElo"], black_elo=game.headers["BlackElo"],
                      white_rating_diff=game.headers["WhiteRatingDiff"],
                      black_rating_diff=game.headers["BlackRatingDiff"], eco=game.headers["ECO"],
                      opening=game.headers["Opening"], time_control=game.headers["TimeControl"],
                      termination=game.headers["Termination"], moves=str(game.mainline_moves())).save()
    os.remove("temp.pgn")


def calculate_percentages(name, params):
    won_games = 0
    lost_games = 0
    drawn_games = 0
    # TODO add empty field check
    """
    games = Games.objects.filter(((Q(white=name) & Q(white_elo__gte=params["elolb"]) &
                                   Q(white_elo__lte=params["eloub"])) | (Q(black=name) &
                                                                         Q(black_elo__gte=params["elolb"]) &
                                                                         Q(white_elo__lte=params["eloub"]))) &
                                 Q(event=params["event"]) & (Q(white=params["opponent"]) | Q(black=params["opponent"]))
                                 & Q(opening=params["opening"]) & Q(termination=params["termination"]) &
                                 Q(eco=params["eco"]) & Q(date__gte=params["periodstart"])
                                 & Q(date__lte=params["periodend"]))
    """
    games = Games.objects.filter(Q(white=name) | Q(black=name))
    for game in games:
        if game.white == name:
            if game.result == "1-0":
                won_games = won_games + 1
            if game.result == "1/2-1/2":
                drawn_games = drawn_games + 1
            if game.result == "0-1":
                lost_games = lost_games + 1
        else:
            if game.result == "0-1":
                won_games = won_games + 1
            if game.result == "1/2-1/2":
                drawn_games = drawn_games + 1
            if game.result == "1-0":
                lost_games = lost_games + 1
    if won_games + lost_games + drawn_games == 0:
        return 0, 0, 0, 0, 0, 0
    percentage_won = (won_games / (won_games + lost_games + drawn_games)) * 100
    percentage_lost = (lost_games / (won_games + lost_games + drawn_games)) * 100
    percentage_drawn = (drawn_games / (won_games + lost_games + drawn_games)) * 100
    return percentage_won, percentage_lost, percentage_drawn, won_games, lost_games, drawn_games


# evaluation isn't perfect, more time you give it the better the result. Results are more precise in middle game
# too slow
def evaluate_games(name):
    games = Games.objects.filter(Q(white=name) | Q(black=name))
    accurate_moves = 0
    moves_played = 0
    for game in games:
        pgn = io.StringIO(game.moves)
        parsed_game = chess.pgn.read_game(pgn)
        engine = chess.engine.SimpleEngine.popen_uci("stockfish_14.1_win_x64_avx2.exe")
        while not parsed_game.is_end():
            node = parsed_game.variations[0]
            result = engine.analysis(parsed_game.board(), chess.engine.Limit(time=0.1))
            # info = engine.analyse(parsed_game.board(), chess.engine.Limit(time=2))
            # t = str(info["score"].pov(info["score"].turn))
            # if t.startswith("#"):
            #    print("Best move: ", parsed_game.board().san(result.wait().move), " eval = mate in", t)
            # else:
            #    print("Best move: ", parsed_game.board().san(result.wait().move), " eval =", round(int(t)/100., 2))
            parsed_game = node
            moves_played = moves_played + 1
            if str(parsed_game.move) == str(result.wait().move):
                accurate_moves = accurate_moves + 1
        engine.quit()
        print(accurate_moves, moves_played)
    return (accurate_moves * 1. / moves_played) * 100
