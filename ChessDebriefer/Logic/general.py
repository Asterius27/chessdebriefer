import datetime
import os
import threading
import chess.pgn
from mongoengine import Q
from ChessDebriefer.models import Games, FieldsCache, Openings, Players


# only works with 1 file upload at a time, and it takes a lot of time to parse everything
def handle_pgn_uploads(f):
    with open('temp.pgn', 'wb+') as temp:
        for chunk in f.chunks():
            temp.write(chunk)
    thr = threading.Thread(target=parse_pgn)
    thr.start()


# check if game already exists in the database?
def parse_pgn():
    cached_fields = FieldsCache.objects.first()
    fields = ["event", "termination"]
    if not cached_fields:
        cached_fields = FieldsCache(event=[], opening_id=[], eco=[], termination=[]).save()
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
                white_player = Players.objects.filter(Q(name=saved_game.white)).first()
                black_player = Players.objects.filter(Q(name=saved_game.black)).first()
                if white_player:
                    if white_player.elo_date < saved_game.date:
                        setattr(white_player, "elo", saved_game.white_elo)
                        setattr(white_player, "elo_date", saved_game.date)
                        white_player.save()
                else:
                    Players(name=saved_game.white, elo=saved_game.white_elo, elo_date=saved_game.date).save()
                if black_player:
                    if black_player.elo_date < saved_game.date:
                        setattr(black_player, "elo", saved_game.white_elo)
                        setattr(black_player, "elo_date", saved_game.date)
                        black_player.save()
                else:
                    Players(name=saved_game.black, elo=saved_game.black_elo, elo_date=saved_game.date).save()
    os.remove("temp.pgn")


def handle_pgn_openings_upload(f):
    cached_fields = FieldsCache.objects.first()
    fields = ["opening_id", "eco"]
    if not cached_fields:
        cached_fields = FieldsCache(event=[], opening_id=[], eco=[], termination=[]).save()
    with open('openings.pgn', 'wb+') as temp:
        for chunk in f.chunks():
            temp.write(chunk)
    Openings.drop_collection()
    with open('openings.pgn') as pgn:
        while True:
            opening = chess.pgn.read_game(pgn)
            if opening is None:
                break
            Openings(eco=opening.headers["Site"], white_opening=opening.headers["White"],
                     black_opening=opening.headers["Black"], moves=str(opening.mainline_moves()), engine_evaluation="",
                     database_evaluation={}).save()
    os.remove("openings.pgn")
    for field in fields:
        setattr(cached_fields, field, [])
    cached_fields.save()
