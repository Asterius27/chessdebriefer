import concurrent.futures
import datetime
import os
import threading
import multiprocessing
import mongoengine
import yappi
from os.path import exists
import chess.pgn
from ChessDebriefer.Logic.games import find_opening
from ChessDebriefer.models import Games, Openings


# TODO add headers check (?)
# it takes a lot of time to parse everything
def handle_pgn_uploads(f):
    if Openings.objects.first() is not None:
        i = 0
        while exists('temp' + str(i) + '.pgn'):
            i += 1
        file_name = 'temp' + str(i) + '.pgn'
        with open(file_name, 'wb+') as temp:
            for chunk in f.chunks():
                temp.write(chunk)
        thr = threading.Thread(target=parse_pgn, args=(file_name, i))
        thr.start()


# 16 min without save and n = 10, 14 min without save and find_opening and n = 20, 3 min with multiprocessing and
# n = 50 and n = 10 and without save and find_opening, 4 min with n = 5 and multiprocessing and without save and
# find_opening

# n = 10 -> 34 min per 121114 partite
# n = 1 -> 1 ora e 49 min per 121114 partite
# n = 10 -> 28 min per 179207 partite with index
# n = 10 -> 19 min per 121114 partite with index
# n = 1 -> 42 min per 121114 partite with index
# n = 20 -> 20 min per 121114 partite with index
# n = 10 -> 20 min per 121114 partite with index and separated files
# n = 20 -> 20 min per 121114 partite with index and separated files
# n = 100 -> 20 min per 121114 partite with index and separated files
# n = 5 -> 11 min per 121114 partite with index and separated files and multiprocessing
# n = 10 -> 9 min per 121114 partite with index and separated files and multiprocessing
def parse_pgn(file_name, ind):
    # cached_fields = FieldsCache.objects.first()
    # fields = ["event", "termination"]
    # if not cached_fields:
    #    cached_fields = FieldsCache(event=[], opening_id=[], eco=[], termination=[]).save()
    with open(file_name) as pgn:
        n = 5
        lines = pgn.readlines()
        l = len(lines)
        j = 0
        h = 0
        file = open("temp" + str(ind) + str(j) + ".pgn", 'w+')
        for i in range(l - 1):
            if lines[i] == "\n" and h > ((l / n) * 1.) and lines[i + 1].startswith("["):
                file.write(lines[i])
                file.close()
                h = 0
                j += 1
                file = open("temp" + str(ind) + str(j) + ".pgn", 'w+')
            else:
                file.write(lines[i])
            h += 1
        file.write(lines[l - 1])
        file.close()
    # yappi.start()
    print(datetime.datetime.now())
    threads = []
    mongoengine.disconnect()
    for x in range(n):
        thr = multiprocessing.Process(target=run, args=(x, ind))
        thr.start()
        threads.append(thr)
    mongoengine.connect(db='ChessDebriefer', host='mongodb://root:root@chessdebrieferdatabase:27017')
    for t in threads:
        t.join()
    os.remove(file_name)
    print(datetime.datetime.now())
    """
    yappi.stop()
    threads = yappi.get_thread_stats()
    for thread in threads:
        print("Function stats for (%s) (%d)" % (thread.name, thread.id))
        yappi.get_func_stats(ctx_id=thread.id).print_all()
        """
    """
        futures = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=n) as executor:
            print(datetime.datetime.now())
            for x in range(n):
                future = executor.submit(run, x, ind)
                futures.append(future)
            concurrent.futures.wait(futures)
    print(datetime.datetime.now())
    os.remove(file_name)
    """


def run(i, ind):
    mongoengine.connect(db='ChessDebriefer', host='mongodb://root:root@chessdebrieferdatabase:27017')
    with open("temp" + str(ind) + str(i) + ".pgn") as pgn:
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
                fen = ""
                if reaches_five_piece_endgame(game):
                    fen = endgame_start_fen(game.end())
                saved_game = Games(event=event, tournament_site=tournament_site, site=game.headers["Site"],
                                   white=game.headers["White"], black=game.headers["Black"],
                                   result=game.headers["Result"], date=date, white_elo=game.headers["WhiteElo"],
                                   black_elo=game.headers["BlackElo"],
                                   white_rating_diff=game.headers["WhiteRatingDiff"],
                                   black_rating_diff=game.headers["BlackRatingDiff"], eco="",
                                   opening_id="000000000000000000000000", time_control=game.headers["TimeControl"],
                                   termination=game.headers["Termination"], moves=str(game.mainline_moves()),
                                   best_moves=[], moves_evaluation=[], five_piece_endgame_fen=fen)
                find_opening(saved_game)
                try:
                    saved_game.save()
                except:
                    saved_game.delete()
                # update_cache(saved_game, fields, cached_fields)
                # update_player_cache(saved_game.white, saved_game.white_elo, saved_game)
                # update_player_cache(saved_game.black, saved_game.black_elo, saved_game)
    os.remove("temp" + str(ind) + str(i) + ".pgn")


def reaches_five_piece_endgame(parsed_game):
    i = 0
    pieces = "rnbqkp"
    fen = parsed_game.end().board().board_fen().lower()
    for char in fen:
        if char in pieces:
            i += 1
        if i > 5:
            return False
    return True


def endgame_start_fen(parsed_game):
    pieces = "rnbqkp"
    while True:
        i = 0
        fen = parsed_game.board().board_fen().lower()
        for char in fen:
            if char in pieces:
                i += 1
        if i > 5:
            end_game_start = parsed_game.variations[0]
            break
        parsed_game = parsed_game.parent
    return end_game_start.board().fen()


def handle_pgn_openings_upload(f):
    # cached_fields = FieldsCache.objects.first()
    # fields = ["opening_id", "eco"]
    # if not cached_fields:
    #    cached_fields = FieldsCache(event=[], opening_id=[], eco=[], termination=[]).save()
    with open('openings.pgn', 'wb+') as temp:
        for chunk in f.chunks():
            temp.write(chunk)
    Openings.drop_collection()
    Games.drop_collection()
    thr = threading.Thread(target=parse_pgn_opening)
    thr.start()
    # for field in fields:
    #    setattr(cached_fields, field, [])
    # cached_fields.save()


def parse_pgn_opening():
    with open('openings.pgn') as pgn:
        n = 10
        lock = threading.Lock()
        futures = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=n) as executor:
            for x in range(n):
                future = executor.submit(run_openings, pgn, lock)
                futures.append(future)
            concurrent.futures.wait(futures)
    os.remove("openings.pgn")


def run_openings(pgn, lock):
    while True:
        with lock:
            opening = chess.pgn.read_game(pgn)
        if opening is None:
            break
        Openings(eco=opening.headers["Site"], white_opening=opening.headers["White"],
                 black_opening=opening.headers["Black"], moves=str(opening.mainline_moves()),
                 engine_evaluation="").save()


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

'''DEPRECATED
def update_player_cache(name, elo, game):
    player = Players.objects.filter(Q(name=name)).first()
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
    if not player:
        player = Players(name=name, elo=elo, elo_date=game.date, accuracy={}).save()
    if player.elo_date < game.date:
        setattr(player, "elo", elo)
        setattr(player, "elo_date", game.date)
    player.save()
'''
