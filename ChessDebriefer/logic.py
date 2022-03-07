import datetime
import io
import os
import re
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


# pretty slow
# TODO add opponent, eco filter
def calculate_percentages(name, params):
    date_pattern = re.compile(r'^\d{4}-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])$')
    elo_pattern = re.compile(r'^\d{1,4}$')
    if not params:
        games = Games.objects.filter(Q(white=name) | Q(black=name))
        white_games = Games.objects.filter(Q(white=name))
        black_games = Games.objects.filter(Q(black=name))
    else:
        if "from" not in params.keys():
            from_date = datetime.datetime(1970, 1, 1)
        else:
            if date_pattern.match(params["from"]):
                date_str = params["from"].split("-")
                try:
                    from_date = datetime.datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))
                except ValueError:
                    from_date = datetime.datetime(1970, 1, 1)
            else:
                from_date = datetime.datetime(1970, 1, 1)
        if "to" not in params.keys():
            to_date = datetime.datetime.now()
        else:
            if date_pattern.match(params["to"]):
                date_str = params["to"].split("-")
                try:
                    to_date = datetime.datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))
                except ValueError:
                    to_date = datetime.datetime.now()
            else:
                to_date = datetime.datetime.now()
        if "minelo" not in params.keys():
            min_elo = 0
        else:
            if elo_pattern.match(params["minelo"]):
                min_elo = int(params["minelo"])
            else:
                min_elo = 0
        if "maxelo" not in params.keys():
            max_elo = 9999  # retrieve highest elo from database and assign it here
        else:
            if elo_pattern.match(params["maxelo"]):
                max_elo = int(params["maxelo"])
            else:
                max_elo = 9999  # retrieve highest elo from database and assign it here
        games = Games.objects.filter(((Q(white=name) & Q(white_elo__gte=min_elo) & Q(white_elo__lte=max_elo)) |
                                      (Q(black=name) & Q(black_elo__gte=min_elo) & Q(black_elo__lte=max_elo)))
                                     & Q(date__gte=from_date) & Q(date__lte=to_date))
        white_games = Games.objects.filter(Q(white=name) & Q(white_elo__gte=min_elo) & Q(white_elo__lte=max_elo)
                                           & Q(date__gte=from_date) & Q(date__lte=to_date))
        black_games = Games.objects.filter(Q(black=name) & Q(black_elo__gte=min_elo) & Q(black_elo__lte=max_elo)
                                           & Q(date__gte=from_date) & Q(date__lte=to_date))
    response = {}
    side_percentages = {}
    general_percentages = create_dictionary(games, name)
    white_percentages = create_dictionary(white_games, name)
    black_percentages = create_dictionary(black_games, name)
    if white_percentages:
        side_percentages["White"] = white_percentages
    if black_percentages:
        side_percentages["Black"] = black_percentages
    event_percentages = filter_games(games, name, "event")
    opening_percentages = filter_games(games, name, "opening")  # does it count only if you are white?
    termination_percentages = filter_games(games, name, "termination")
    throw_percentages = thrown_games(games, name)
    if general_percentages:
        response["General percentages"] = general_percentages
    if side_percentages:
        response["Side percentages"] = side_percentages
    if event_percentages:
        response["Event percentages"] = event_percentages
    if opening_percentages:
        response["Opening percentages"] = opening_percentages
    if termination_percentages:
        response["Termination percentages"] = termination_percentages
    if throw_percentages:
        response["Thrown games percentages"] = throw_percentages
    return response


def filter_games(games, name, field):
    temps = Games.objects()
    fields = []
    result = {}
    for temp in temps:
        if "https" in getattr(temp, field):
            new = temp.event.split(" ")
            del new[-1]
            if ' '.join(new) not in fields:
                fields.append(' '.join(new))
        elif getattr(temp, field) not in fields:
            fields.append(getattr(temp, field))
    for fld in fields:
        filtered_games = filter(lambda game: getattr(game, field) == fld, games)
        dictionary = create_dictionary(filtered_games, name)
        if dictionary:
            result[str(fld)] = dictionary
    return result


def create_dictionary(games, name):
    won_games = 0
    lost_games = 0
    drawn_games = 0
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
        return {}
    percentage_won = round((won_games / (won_games + lost_games + drawn_games)) * 100, 2)
    percentage_lost = round((lost_games / (won_games + lost_games + drawn_games)) * 100, 2)
    percentage_drawn = round((drawn_games / (won_games + lost_games + drawn_games)) * 100, 2)
    return {"percentage_won": percentage_won, "percentage_lost": percentage_lost, "percentage_drawn": percentage_drawn,
            "won_games": won_games, "lost_games": lost_games, "drawn_games": drawn_games}


# evaluation isn't perfect, more time you give it the better the result. Results are more precise in middle game
# only evaluates in centipawns
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


# slow
# TODO add epic comebacks (win from a disadvantage)
def thrown_games(games, name):
    throws = 0
    losses = 0
    for game in games:
        if (game.white == name and game.result == "0-1") or (game.black == name and game.result == "1-0"):
            cp = average_game_centipawn(game, name)
            losses = losses + 1
            if cp > 0:
                throws = throws + 1
            print(throws, losses, cp)
    percentage = round((throws * 1. / losses) * 100, 2)
    return {"throws": throws, "losses": losses, "percentage": percentage}


def average_game_centipawn(game, name):
    moves = 0
    centipawn = 0
    parsed_game = chess.pgn.read_game(io.StringIO(game.moves))
    engine = chess.engine.SimpleEngine.popen_uci("stockfish_14.1_win_x64_avx2.exe")
    while not parsed_game.is_end():
        node = parsed_game.variations[0]
        if node.turn() and game.white == name:
            info = engine.analyse(parsed_game.board(), chess.engine.Limit(time=1))
            if not str(info["score"].pov(True)).startswith("#"):
                centipawn = centipawn + int(str(info["score"].pov(True)))
                moves = moves + 1
        if not node.turn() and game.black == name:
            info = engine.analyse(parsed_game.board(), chess.engine.Limit(time=1))
            if not str(info["score"].pov(False)).startswith("#"):
                centipawn = centipawn + int(str(info["score"].pov(False)))
                moves = moves + 1
        parsed_game = node
    engine.quit()
    return round(centipawn * 1. / moves, 2)
