import datetime
import os
import threading
from os.path import exists
import chess.pgn
from mongoengine import Q
from ChessDebriefer.Logic.games import find_opening
from ChessDebriefer.models import Games, Openings, Players


# TODO add check if file is a pgn, check headers
# it takes a lot of time to parse everything
def handle_pgn_uploads(f):
    i = 0
    while exists('temp' + str(i) + '.pgn'):
        i += 1
    file_name = 'temp' + str(i) + '.pgn'
    with open(file_name, 'wb+') as temp:
        for chunk in f.chunks():
            temp.write(chunk)
    thr = threading.Thread(target=parse_pgn, args=(file_name,))
    thr.start()


def parse_pgn(file_name):
    # cached_fields = FieldsCache.objects.first()
    # fields = ["event", "termination"]
    # if not cached_fields:
    #    cached_fields = FieldsCache(event=[], opening_id=[], eco=[], termination=[]).save()
    with open(file_name) as pgn:
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break
            if game.headers["Black"] != "?" and game.headers["White"] != "?" and game.headers["UTCDate"] != "?" and \
                    game.headers["UTCTime"] != "?":
                arr_date = game.headers["UTCDate"].split(".")
                arr_time = game.headers["UTCTime"].split(":")
                date = datetime.datetime(int(arr_date[0]), int(arr_date[1]), int(arr_date[2]), int(arr_time[0]),
                                         int(arr_time[1]), int(arr_time[2]))
                if "https" in game.headers["Event"]:
                    temp = game.headers["Event"].split(" ")
                    tournament_site = temp[-1]
                    del temp[-1]
                    event = ' '.join(temp)
                else:
                    tournament_site = ""
                    event = game.headers["Event"]
                exist = Games.objects.filter(Q(event=event) & Q(tournament_site=tournament_site) &
                                             Q(site=game.headers["Site"]) & Q(white=game.headers["White"]) &
                                             Q(black=game.headers["Black"]) & Q(result=game.headers["Result"]) &
                                             Q(date=date) & Q(white_elo=game.headers["WhiteElo"]) &
                                             Q(black_elo=game.headers["BlackElo"]) &
                                             Q(white_rating_diff=game.headers["WhiteRatingDiff"]) &
                                             Q(black_rating_diff=game.headers["BlackRatingDiff"]) &
                                             Q(time_control=game.headers["TimeControl"]) &
                                             Q(termination=game.headers["Termination"]) &
                                             Q(moves=str(game.mainline_moves()))).first()
                if not exist:
                    saved_game = Games(event=event, tournament_site=tournament_site, site=game.headers["Site"],
                                       white=game.headers["White"], black=game.headers["Black"],
                                       result=game.headers["Result"], date=date, white_elo=game.headers["WhiteElo"],
                                       black_elo=game.headers["BlackElo"],
                                       white_rating_diff=game.headers["WhiteRatingDiff"],
                                       black_rating_diff=game.headers["BlackRatingDiff"], eco="",
                                       opening_id="000000000000000000000000", time_control=game.headers["TimeControl"],
                                       termination=game.headers["Termination"], moves=str(game.mainline_moves()),
                                       best_moves=[], moves_evaluation=[]).save()
                    find_opening(saved_game)
                    # update_cache(saved_game, fields, cached_fields)
                    update_player_cache(saved_game.white, saved_game.white_elo, saved_game)
                    update_player_cache(saved_game.black, saved_game.black_elo, saved_game)
    os.remove(file_name)


'''DEPRECATED
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
    update_player_cache(game.white, game.white_elo, game)
    update_player_cache(game.black, game.black_elo, game)
'''


def update_player_cache(name, elo, game):
    player = Players.objects.filter(Q(name=name)).first()
    '''
    if "https" in game.event:
        new = game.event.split(" ")
        del new[-1]
        event = ' '.join(new)
    else:
        event = game.event
    if not player:
        player = Players(name=name, elo=elo, elo_date=game.date, openings={}, terminations={}, events={}, accuracy={},
                         percentages={}).save()
    if not player.percentages:
        player.percentages = {"general percentages": {"wins": 0, "losses": 0, "draws": 0},
                              "side percentages": {"white": {"wins": 0, "losses": 0, "draws": 0},
                                                   "black": {"wins": 0, "losses": 0, "draws": 0}}}
    if game.termination not in player.terminations.keys():
        player.terminations[game.termination] = {"wins": 0, "losses": 0, "draws": 0}
    if event not in player.events.keys():
        player.events[event] = {"wins": 0, "losses": 0, "draws": 0}
    if game.eco not in player.openings.keys():
        player.openings[game.eco] = {"wins": 0, "losses": 0, "draws": 0}
    if game.white == name:
        if game.result == "1-0":
            player.percentages["general percentages"]["wins"] += 1
            player.percentages["side percentages"]["white"]["wins"] += 1
            player.events[event]["wins"] += 1
            player.terminations[game.termination]["wins"] += 1
            player.openings[game.eco]["wins"] += 1
        if game.result == "0-1":
            player.percentages["general percentages"]["losses"] += 1
            player.percentages["side percentages"]["white"]["losses"] += 1
            player.events[event]["losses"] += 1
            player.terminations[game.termination]["losses"] += 1
            player.openings[game.eco]["losses"] += 1
        if game.result == "1/2-1/2":
            player.percentages["general percentages"]["draws"] += 1
            player.percentages["side percentages"]["white"]["draws"] += 1
            player.events[event]["draws"] += 1
            player.terminations[game.termination]["draws"] += 1
            player.openings[game.eco]["draws"] += 1
    if game.black == name:
        if game.result == "0-1":
            player.percentages["general percentages"]["wins"] += 1
            player.percentages["side percentages"]["black"]["wins"] += 1
            player.events[event]["wins"] += 1
            player.terminations[game.termination]["wins"] += 1
            player.openings[game.eco]["wins"] += 1
        if game.result == "1-0":
            player.percentages["general percentages"]["losses"] += 1
            player.percentages["side percentages"]["black"]["losses"] += 1
            player.events[event]["losses"] += 1
            player.terminations[game.termination]["losses"] += 1
            player.openings[game.eco]["losses"] += 1
        if game.result == "1/2-1/2":
            player.percentages["general percentages"]["draws"] += 1
            player.percentages["side percentages"]["black"]["draws"] += 1
            player.events[event]["draws"] += 1
            player.terminations[game.termination]["draws"] += 1
            player.openings[game.eco]["draws"] += 1
    '''
    if not player:
        player = Players(name=name, elo=elo, elo_date=game.date, accuracy={}).save()
    if player.elo_date < game.date:
        setattr(player, "elo", elo)
        setattr(player, "elo_date", game.date)
    player.save()


def handle_pgn_openings_upload(f):
    # cached_fields = FieldsCache.objects.first()
    # fields = ["opening_id", "eco"]
    # if not cached_fields:
    #    cached_fields = FieldsCache(event=[], opening_id=[], eco=[], termination=[]).save()
    with open('openings.pgn', 'wb+') as temp:
        for chunk in f.chunks():
            temp.write(chunk)
    Openings.drop_collection()
    thr = threading.Thread(target=parse_pgn_opening)
    thr.start()
    # for field in fields:
    #    setattr(cached_fields, field, [])
    # cached_fields.save()


def parse_pgn_opening():
    with open('openings.pgn') as pgn:
        while True:
            opening = chess.pgn.read_game(pgn)
            if opening is None:
                break
            Openings(eco=opening.headers["Site"], white_opening=opening.headers["White"],
                     black_opening=opening.headers["Black"], moves=str(opening.mainline_moves()),
                     engine_evaluation="").save()
    os.remove("openings.pgn")