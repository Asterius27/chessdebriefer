import datetime
import os
import threading
import chess.pgn
from mongoengine import Q
from ChessDebriefer.Logic.games import find_opening
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
                find_opening(saved_game)
                update_cache(saved_game, fields, cached_fields)
    os.remove("temp.pgn")


def update_cache(game, fields, cached_fields):
    for field in fields:
        if "https" in getattr(game, field):
            new = game.event.split(" ")
            del new[-1]
            if ' '.join(new) not in getattr(cached_fields, field):
                temp = getattr(cached_fields, field)
                temp.append(' '.join(new))
                setattr(cached_fields, field, temp)
                cached_fields.save()
        elif getattr(game, field) not in getattr(cached_fields, field):
            temp = getattr(cached_fields, field)
            temp.append(getattr(game, field))
            setattr(cached_fields, field, temp)
            cached_fields.save()
    white_player = Players.objects.filter(Q(name=game.white)).first()
    black_player = Players.objects.filter(Q(name=game.black)).first()
    if not white_player:
        white_player = Players(name=game.white, elo=game.white_elo, elo_date=game.date, openings={}).save()
    if game.eco not in white_player.openings.keys():
        white_player.openings[game.eco] = {"wins": 0, "losses": 0, "draws": 0}
    if game.result == "1-0":
        white_player.openings[game.eco]["wins"] += 1
    if game.result == "0-1":
        white_player.openings[game.eco]["losses"] += 1
    if game.result == "1/2-1/2":
        white_player.openings[game.eco]["draws"] += 1
    if white_player.elo_date < game.date:
        setattr(white_player, "elo", game.white_elo)
        setattr(white_player, "elo_date", game.date)
    white_player.save()
    if not black_player:
        black_player = Players(name=game.black, elo=game.black_elo, elo_date=game.date, openings={}).save()
    if game.eco not in black_player.openings.keys():
        black_player.openings[game.eco] = {"wins": 0, "losses": 0, "draws": 0}
    if game.result == "0-1":
        black_player.openings[game.eco]["wins"] += 1
    if game.result == "1-0":
        black_player.openings[game.eco]["losses"] += 1
    if game.result == "1/2-1/2":
        black_player.openings[game.eco]["draws"] += 1
    if black_player.elo_date < game.date:
        setattr(black_player, "elo", game.white_elo)
        setattr(black_player, "elo_date", game.date)
    black_player.save()


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
