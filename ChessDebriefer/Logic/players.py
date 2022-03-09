import datetime
import re
from mongoengine import Q
from ChessDebriefer.Logic.games import evaluate_game, average_game_centipawn
from ChessDebriefer.models import Games, FieldsCache, Players


# pretty slow, caching only works without query params
# TODO add opponent, eco filter
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
    throw_comeback_percentages = filter_throws_comebacks(games, name)
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
    if throw_comeback_percentages:
        response["Throw comeback percentages"] = throw_comeback_percentages
    if cache_flag:
        Players(name=name, percentages=response).save()
    return response


def filter_games(games, name, field):
    fields_cache = FieldsCache.objects.first()
    result = {}
    for fld in getattr(fields_cache, field):
        filtered_games = filter(lambda game: getattr(game, field) == fld, games)
        dictionary = create_dictionary(filtered_games, name)
        if field == "opening" and dictionary:
            list_filtered_games = list(filter(lambda game: getattr(game, field) == fld, games))
            dictionary["event"] = event_filter(list_filtered_games, name)
        if dictionary:
            result[str(fld)] = dictionary
    return result


def event_filter(games, name):
    events = getattr(FieldsCache.objects.first(), "event")
    result = {}
    for event in events:
        filtered_games = filter(lambda game: getattr(game, "event") == event, games)
        dictionary = create_dictionary(filtered_games, name)
        if dictionary:
            result[str(event)] = dictionary
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


def filter_throws_comebacks(games, name):
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


def calculate_accuracy(name):
    accuracy = 0
    total_moves = 0
    games = Games.objects.filter(Q(white=name) | Q(black=name))
    for game in games:
        i = 0
        if not game.best_moves:
            evaluate_game(game)
        temp = game.moves.split(" ")
        pattern = re.compile(r'\.$')
        moves = list(filter(lambda m: not pattern.search(m), temp))
        if game.white == name:
            for (move, best_move) in zip(moves, game.best_moves):
                if i % 2 == 0:
                    if move == best_move:
                        accuracy = accuracy + 1
                    total_moves = total_moves + 1
                i = i + 1
        if game.black == name:
            for (move, best_move) in zip(moves, game.best_moves):
                if i % 2 != 0:
                    if move == best_move:
                        accuracy = accuracy + 1
                    total_moves = total_moves + 1
                i = i + 1
    return round(((accuracy * 1.) / total_moves) * 100, 2)
