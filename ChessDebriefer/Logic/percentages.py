import datetime
import re
from mongoengine import Q
from ChessDebriefer.Logic.games import average_game_centipawn, find_opening
from ChessDebriefer.models import Games, FieldsCache, Players

'''DEPRECATED'''


def calculate_percentages(name, params):
    games, white_games, black_games = database_query(name, params)
    response = {}
    side_percentages = {}
    general_percentages = create_dictionary(games, name)
    white_percentages = create_dictionary(white_games, name)
    black_percentages = create_dictionary(black_games, name)
    throw_comeback_percentages = {}  # filter_throws_comebacks(games, name)
    if white_percentages:
        side_percentages["White"] = white_percentages
    if black_percentages:
        side_percentages["Black"] = black_percentages
    if general_percentages:
        response["General percentages"] = general_percentages
    if side_percentages:
        response["Side percentages"] = side_percentages
    if throw_comeback_percentages:
        response["Throw comeback percentages"] = throw_comeback_percentages
    return response


def calculate_event_percentages(name, params):
    if params:
        games, white_games, black_games = database_query(name, params)
        return filter_games(games, name, "event")
    else:
        return cached_response("events", name)


# TODO add from to eco query, ex. A01..B30
def calculate_opening_percentages(name, params):
    games, white_games, black_games = database_query(name, params)
    if "eco" not in params.keys():
        return filter_games(games, name, "eco")
    else:
        dictionary = {}
        ecos = params["eco"].split(",")
        side_dict = {}
        filtered_games = list(filter(lambda g: g.eco in ecos, games))
        filtered_white_games = list(filter(lambda g: g.eco in ecos, white_games))
        filtered_black_games = list(filter(lambda g: g.eco in ecos, black_games))
        general_dict = create_dictionary(filtered_games, name)
        white_dict = create_dictionary(filtered_white_games, name)
        black_dict = create_dictionary(filtered_black_games, name)
        if general_dict:
            dictionary["general stats"] = general_dict
            dictionary["events"] = event_filter(filtered_games, name)
        if white_dict:
            side_dict["white"] = white_dict
            side_dict["white events"] = event_filter(filtered_white_games, name)
        if black_dict:
            side_dict["black"] = black_dict
            side_dict["black events"] = event_filter(filtered_black_games, name)
        if side_dict:
            dictionary["side stats"] = side_dict
        return dictionary


def calculate_termination_percentages(name, params):
    if params:
        games, white_games, black_games = database_query(name, params)
        return filter_games(games, name, "termination")
    else:
        return cached_response("terminations", name)


def cached_response(attribute, name):
    response = {}
    player = Players.objects.filter(Q(name=name)).first()
    dictionary = getattr(player, attribute)
    for key in dictionary.keys():
        percentage_won = round((dictionary[key]["wins"] / (dictionary[key]["wins"] + dictionary[key]["losses"] +
                                                           dictionary[key]["draws"])) * 100, 2)
        percentage_lost = round((dictionary[key]["losses"] / (dictionary[key]["wins"] + dictionary[key]["losses"] +
                                                              dictionary[key]["draws"])) * 100, 2)
        percentage_drawn = round((dictionary[key]["draws"] / (dictionary[key]["wins"] + dictionary[key]["losses"] +
                                                              dictionary[key]["draws"])) * 100, 2)
        response[key] = player.terminations[key]
        # response[key] = player.events[key]
        response[key]["percentage won"] = percentage_won
        response[key]["percentage lost"] = percentage_lost
        response[key]["percentage drawn"] = percentage_drawn
    return response


def database_query(name, params):
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
        if "opponent" not in params.keys():
            games = Games.objects.filter(((Q(white=name) & Q(white_elo__gte=min_elo) & Q(white_elo__lte=max_elo)) |
                                          (Q(black=name) & Q(black_elo__gte=min_elo) & Q(black_elo__lte=max_elo)))
                                         & Q(date__gte=from_date) & Q(date__lte=to_date))
            white_games = Games.objects.filter(Q(white=name) & Q(white_elo__gte=min_elo) & Q(white_elo__lte=max_elo)
                                               & Q(date__gte=from_date) & Q(date__lte=to_date))
            black_games = Games.objects.filter(Q(black=name) & Q(black_elo__gte=min_elo) & Q(black_elo__lte=max_elo)
                                               & Q(date__gte=from_date) & Q(date__lte=to_date))
        else:
            games = Games.objects.filter(((Q(white=name) & Q(black=params["opponent"]) & Q(white_elo__gte=min_elo) &
                                           Q(white_elo__lte=max_elo)) | (Q(black=name) & Q(white=params["opponent"]) &
                                                                         Q(black_elo__gte=min_elo) &
                                                                         Q(black_elo__lte=max_elo)))
                                         & Q(date__gte=from_date) & Q(date__lte=to_date))
            white_games = Games.objects.filter(Q(white=name) & Q(black=params["opponent"]) & Q(white_elo__gte=min_elo)
                                               & Q(white_elo__lte=max_elo) & Q(date__gte=from_date)
                                               & Q(date__lte=to_date))
            black_games = Games.objects.filter(Q(black=name) & Q(white=params["opponent"]) & Q(black_elo__gte=min_elo)
                                               & Q(black_elo__lte=max_elo) & Q(date__gte=from_date)
                                               & Q(date__lte=to_date))
    for game in games:
        find_opening(game)
    return games, white_games, black_games


def filter_games(games, name, field):
    fields_cache = FieldsCache.objects.first()
    result = {}
    for fld in getattr(fields_cache, field):
        filtered_games = filter(lambda game: getattr(game, field).startswith(fld), games)
        dictionary = create_dictionary(filtered_games, name)
        if field == "eco" and dictionary:
            list_filtered_games = list(filter(lambda game: getattr(game, field).startswith(fld), games))
            dictionary["events"] = event_filter(list_filtered_games, name)
        if dictionary:
            result[str(fld)] = dictionary
    return result


def event_filter(games, name):
    events = getattr(FieldsCache.objects.first(), "event")
    result = {}
    for event in events:
        filtered_games = filter(lambda game: getattr(game, "event").startswith(event), games)
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
    comebacks = 0
    losses = 0
    wins = 0
    percentage_throws = 0
    percentage_comebacks = 0
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
    if losses != 0:
        percentage_throws = round((throws * 1. / losses) * 100, 2)
    if wins != 0:
        percentage_comebacks = round((comebacks * 1. / wins) * 100, 2)
    if wins == 0 and losses == 0:
        return {}
    return {"throws": throws, "losses": losses, "percentage_throws": percentage_throws, "comebacks": comebacks,
            "wins": wins, "percentage_comebacks": percentage_comebacks}
