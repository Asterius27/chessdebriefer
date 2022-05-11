import bz2
import concurrent.futures
import datetime
import os
import shutil
import threading
import multiprocessing
import mongoengine
from os.path import exists
import chess.pgn
from ChessDebriefer.Logic.games import find_opening
from ChessDebriefer.models import Games, Openings


# TODO add headers check (?)
def handle_pgn_uploads(f):
    if Openings.objects.first() is not None:
        if str(f).endswith('.bz2'):
            i = 0
            j = 0
            while exists('temp' + str(i) + '.bz2'):
                i += 1
            compressed_file_name = 'temp' + str(i) + '.bz2'
            with open(compressed_file_name, 'wb+') as temp:
                for chunk in f.chunks():
                    temp.write(chunk)
            while exists('temp' + str(j) + '.pgn'):
                j += 1
            file_name = 'temp' + str(j) + '.pgn'
            thr = threading.Thread(target=parse_pgn, args=(file_name, compressed_file_name, j))
            thr.start()
        if str(f).endswith('.pgn'):  # request.FILES['file'].content_type == "application/x-chess-pgn"
            i = 0
            while exists('temp' + str(i) + '.pgn'):
                i += 1
            file_name = 'temp' + str(i) + '.pgn'
            with open(file_name, 'wb+') as temp:
                for chunk in f.chunks():
                    temp.write(chunk)
            thr = threading.Thread(target=parse_pgn, args=(file_name, "", i))
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
def parse_pgn(file_name, compressed_file_name, ind):
    if compressed_file_name != "":
        with bz2.BZ2File(compressed_file_name) as fr, open(file_name, 'wb') as fw:
            shutil.copyfileobj(fr, fw)
        os.remove(compressed_file_name)
    with open(file_name) as pgn:
        n = 25
        flag = False
        j = 0
        file = open("temp" + str(ind) + str(j) + ".pgn", 'a+')
        for line in pgn:
            if line == "\n" and flag:
                file.write(line)
                file.close()
                j += 1
                if j == n:
                    j = 0
                file = open("temp" + str(ind) + str(j) + ".pgn", 'a+')
                flag = False
            elif line == "\n" and not flag:
                file.write(line)
                flag = True
            elif line != "\n":
                file.write(line)
        file.close()
    print(datetime.datetime.now())
    processes = []
    mongoengine.disconnect()
    for x in range(n):
        prc = multiprocessing.Process(target=run, args=(x, ind))
        prc.start()
        processes.append(prc)
    mongoengine.connect(db='ChessDebriefer', host='mongodb://root:root@chessdebrieferdatabase:27017')
    for p in processes:
        p.join()
    os.remove(file_name)
    print(datetime.datetime.now())


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
    with open('openings.pgn', 'wb+') as temp:
        for chunk in f.chunks():
            temp.write(chunk)
    Openings.drop_collection()
    Games.drop_collection()
    thr = threading.Thread(target=parse_pgn_opening)
    thr.start()


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
