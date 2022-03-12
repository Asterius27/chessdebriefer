import datetime
import os
import chess.pgn
from ChessDebriefer.models import Games, FieldsCache, Openings


# only works with 1 file upload at a time, and it takes a lot of time to parse everything
def handle_pgn_uploads(f):
    cached_fields = FieldsCache.objects.first()
    fields = ["event", "termination"]
    if not cached_fields:
        cached_fields = FieldsCache(event=[], opening_id=[], eco=[], termination=[]).save()
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
                                   black_rating_diff=game.headers["BlackRatingDiff"], eco="",
                                   opening_id="000000000000000000000000", time_control=game.headers["TimeControl"],
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
    os.remove("temp.pgn")


def handle_pgn_openings_upload(f):
    with open('openings.pgn', 'wb+') as temp:
        for chunk in f.chunks():
            temp.write(chunk)
    with open('openings.pgn') as pgn:
        while True:
            opening = chess.pgn.read_game(pgn)
            if opening is None:
                break
            Openings(eco=opening.headers["Site"], white_opening=opening.headers["White"],
                     black_opening=opening.headers["Black"], moves=str(opening.mainline_moves())).save()
    os.remove("openings.pgn")
