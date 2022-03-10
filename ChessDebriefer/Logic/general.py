import datetime
import os
import chess.pgn
from ChessDebriefer.models import Games, Players, FieldsCache


# only works with 1 file upload at a time, and it takes a lot of time to parse everything
def handle_pgn_uploads(f):
    cached_players = Players.objects
    cached_fields = FieldsCache.objects.first()
    fields = ["event", "opening", "termination"]
    if not cached_fields:
        cached_fields = FieldsCache(event=[], opening=[], termination=[]).save()
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
                saved_game = Games(event=game.headers["Event"], site=game.headers["Site"], white=game.headers["White"],
                                   black=game.headers["Black"], result=game.headers["Result"], date=date,
                                   white_elo=game.headers["WhiteElo"], black_elo=game.headers["BlackElo"],
                                   white_rating_diff=game.headers["WhiteRatingDiff"],
                                   black_rating_diff=game.headers["BlackRatingDiff"], eco=game.headers["ECO"],
                                   opening=game.headers["Opening"], time_control=game.headers["TimeControl"],
                                   termination=game.headers["Termination"], moves=str(game.mainline_moves()),
                                   best_moves=[], moves_evaluation=[]).save()
                for field in fields:
                    if "https" in getattr(saved_game, field):
                        new = saved_game.event.split(" ")
                        del new[-1]
                        if ' '.join(new) not in getattr(cached_fields, field):
                            temp = getattr(cached_fields, field)
                            temp.append(' '.join(new))
                            setattr(cached_fields, field, temp)
                            cached_fields.save()
                    elif getattr(saved_game, field) not in getattr(cached_fields, field):
                        temp = getattr(cached_fields, field)
                        temp.append(getattr(saved_game, field))
                        setattr(cached_fields, field, temp)
                        cached_fields.save()
                for player in cached_players:
                    if saved_game.white == player.name or saved_game.black == player.name:
                        player.delete()
    os.remove("temp.pgn")