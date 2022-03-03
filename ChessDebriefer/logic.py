import datetime
import os
import chess.pgn
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
