import datetime
import io
import os
import re
import chess.pgn
import chess.engine
from mongoengine import Q
from ChessDebriefer.models import Games, Players, FieldsCache


# only works with 1 file upload at a time, and it takes a lot of time to parse everything
# TODO update cache
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
                      termination=game.headers["Termination"], moves=str(game.mainline_moves()), best_moves=[],
                      moves_evaluation=[]).save()
    os.remove("temp.pgn")


# pretty slow, caching only works without query params
# TODO add opponent, eco filter; add openings filtered by event type
def calculate_percentages(name, params):
    date_pattern = re.compile(r'^\d{4}-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])$')
    elo_pattern = re.compile(r'^\d{1,4}$')
    if not params:
        cached_response = Players.objects(name=name).first()
        if not cached_response:
            cache_flag = True
            games = Games.objects.filter(Q(white=name) | Q(black=name))
            white_games = Games.objects.filter(Q(white=name))
            black_games = Games.objects.filter(Q(black=name))
        else:
            return cached_response.percentages
    else:
        cache_flag = False
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
    throw_percentages = throw_comeback_percentages(games, name)
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
    if cache_flag:
        Players(name=name, percentages=response).save()
    return response


def filter_games(games, name, field):
    fields_cache = FieldsCache.objects.first()
    if not fields_cache:
        fields_cache = FieldsCache(event=[], opening=[], termination=[]).save()
    result = {}
    if not getattr(fields_cache, field):
        temps = Games.objects()
        fields = []
        for temp in temps:
            if "https" in getattr(temp, field):
                new = temp.event.split(" ")
                del new[-1]
                if ' '.join(new) not in fields:
                    fields.append(' '.join(new))
            elif getattr(temp, field) not in fields:
                fields.append(getattr(temp, field))
        setattr(fields_cache, field, fields)
        fields_cache.save()
    else:
        fields = getattr(fields_cache, field)
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


def throw_comeback_percentages(games, name):
    throws = 0
    losses = 0
    wins = 0
    comebacks = 0
    for game in games:
        if (game.white == name and game.result == "0-1") or (game.black == name and game.result == "1-0"):
            cp = average_game_centipawn(game, name)
            losses = losses + 1
            if cp > 0:
                throws = throws + 1
        if (game.white == name and game.result == "1-0") or (game.black == name and game.result == "0-1"):
            cp = average_game_centipawn(game, name)
            wins = wins + 1
            if cp < 0:
                comebacks = comebacks + 1
    percentage_throws = round((throws * 1. / losses) * 100, 2)
    percentage_comebacks = round((comebacks * 1. / wins) * 100, 2)
    return {"throws": throws, "losses": losses, "percentage_throws": percentage_throws, "comebacks": comebacks,
            "wins": wins, "percentage_comebacks": percentage_comebacks}


# evaluation isn't perfect, more time you give it the better the result. Results are more precise in middle game
# only evaluates in centipawns, positive means an advantage for white, negative means an advantage for black
# slow
# TODO test caching
def evaluate_game(game):
    pgn = io.StringIO(game.moves)
    parsed_game = chess.pgn.read_game(pgn)
    engine = chess.engine.SimpleEngine.popen_uci("stockfish_14.1_win_x64_avx2.exe")
    best_moves = []
    moves_evaluation = []
    while not parsed_game.is_end():
        node = parsed_game.variations[0]
        result = engine.analysis(parsed_game.board(), chess.engine.Limit(time=1))
        info = engine.analyse(parsed_game.board(), chess.engine.Limit(time=1))
        t = str(info["score"].pov(True))
        best_moves.append(parsed_game.board().san(result.wait().move))
        if t.startswith("#"):
            moves_evaluation.append(t)
        else:
            moves_evaluation.append(str(round(int(t)/100., 2)))
        parsed_game = node
    engine.quit()
    setattr(game, "best_moves", best_moves)
    setattr(game, "moves_evaluation", moves_evaluation)
    game.save()


def average_game_centipawn(game, name):
    moves = 0
    centipawn = 0.
    if not game.moves_evaluation:
        evaluate_game(game)
    it = iter(game.moves_evaluation)
    if game.white == name:
        for evaluation in game.moves_evaluation:
            if not evaluation.startswith("#"):
                centipawn = centipawn + float(evaluation)
                moves = moves + 1
            next(it)
    if game.black == name:
        for evaluation in game.moves_evaluation:
            next(it)
            if not evaluation.startswith("#"):
                centipawn = centipawn + (float(evaluation) * -1)
                moves = moves + 1
    return round(centipawn / moves, 2)


# TODO test it
def calculate_accuracy(name):
    accuracy = 0
    total_moves = 0
    games = Games.objects.filter(Q(white=name) | Q(black=name))
    for game in games:
        if not game.best_moves:
            evaluate_game(game)
        temp = game.moves.split(" ")
        pattern = re.compile(r'\.$')
        moves = filter(lambda m: not pattern.match(m), temp)
        it1 = iter(game.best_moves)
        it2 = iter(moves)
        if game.white == name:
            for (move, best_move) in zip(moves, game.best_moves):
                if move == best_move:
                    accuracy = accuracy + 1
                total_moves = total_moves + 1
                next(it1)
                next(it2)
        if game.black == name:
            for (move, best_move) in zip(moves, game.best_moves):
                next(it1)
                next(it2)
                if move == best_move:
                    accuracy = accuracy + 1
                total_moves = total_moves + 1
    return round(((accuracy * 1.) / total_moves) * 100, 2)
