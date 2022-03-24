import datetime
import re
from mongoengine import Q
from ChessDebriefer.Logic.games import average_game_centipawn, find_opening
from ChessDebriefer.models import Games, FieldsCache, Players


def calculate_percentages(name, params):
    games, white_games, black_games = database_query(name, params)
    response = {}
    side_percentages = {}
    general_percentages = create_dictionary(games, name)
    white_percentages = create_dictionary(white_games, name)
    black_percentages = create_dictionary(black_games, name)
    throw_comeback_percentages = filter_throws_comebacks(games, name)
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


# TODO test it
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


# TODO test it
def calculate_termination_percentages(name, params):
    if params:
        games, white_games, black_games = database_query(name, params)
        return filter_games(games, name, "termination")
    else:
        return cached_response("terminations", name)


# TODO test it
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
        response[key]["percentage won"] = percentage_won
        response[key]["percentage lost"] = percentage_lost
        response[key]["percentage drawn"] = percentage_drawn
    return response


# group by?
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


# TODO find a way to retrieve player elo with a query on Games, without using Players
def calculate_opening_comparisons(name, params):
    response = {}
    if "elo" in params.keys():
        elo = params["elo"]
    else:
        player = Games.objects.filter(Q(white=name) | Q(black=name)).order_by('-date').first()
        if player:
            if player.white == name:
                elo = player.white_elo
            else:
                elo = player.black_elo
        else:
            elo = 0
    if "range" in params.keys():
        r = params["range"]
    else:
        r = 100
    if "eco" in params.keys():
        ecos = params["eco"].split(",")
        player_eco_stats = Games.objects.aggregate([
            {
                '$match': {'$and': [{'$or': [{'white': name}, {'black': name}]}, {'eco': {'$in': ecos}}]}
            },
            {
                '$project': {
                    'eco': 1,
                    'win': {'$cond': {'if': {'$or': [
                        {'$and': [{'$eq': ['$result', '1-0']}, {'$eq': ['$white', name]}]},
                        {'$and': [{'$eq': ['$result', '0-1']}, {'$eq': ['$black', name]}]}
                    ]}, 'then': 1, 'else': 0}},
                    'loss': {'$cond': {'if': {'$or': [
                        {'$and': [{'$eq': ['$result', '1-0']}, {'$eq': ['$black', name]}]},
                        {'$and': [{'$eq': ['$result', '0-1']}, {'$eq': ['$white', name]}]}
                    ]}, 'then': 1, 'else': 0}},
                    'draw': {'$cond': {'if': {'$eq': ['$result', '1/2-1/2']}, 'then': 1, 'else': 0}}
                }
            },
            {
                '$group': {
                    '_id': '$eco',
                    'wins': {'$sum': '$win'},
                    'losses': {'$sum': '$loss'},
                    'draws': {'$sum': '$draw'}
                }
            }
        ])
        player_eco_stats_list = list(player_eco_stats)
    else:
        player_eco_stats = Games.objects.aggregate([
            {
                '$match': {'$or': [{'white': name}, {'black': name}]}
            },
            {
                '$project': {
                    'eco': 1,
                    'win': {'$cond': {'if': {'$or': [
                        {'$and': [{'$eq': ['$result', '1-0']}, {'$eq': ['$white', name]}]},
                        {'$and': [{'$eq': ['$result', '0-1']}, {'$eq': ['$black', name]}]}
                    ]}, 'then': 1, 'else': 0}},
                    'loss': {'$cond': {'if': {'$or': [
                        {'$and': [{'$eq': ['$result', '1-0']}, {'$eq': ['$black', name]}]},
                        {'$and': [{'$eq': ['$result', '0-1']}, {'$eq': ['$white', name]}]}
                    ]}, 'then': 1, 'else': 0}},
                    'draw': {'$cond': {'if': {'$eq': ['$result', '1/2-1/2']}, 'then': 1, 'else': 0}}
                }
            },
            {
                '$group': {
                    '_id': '$eco',
                    'wins': {'$sum': '$win'},
                    'losses': {'$sum': '$loss'},
                    'draws': {'$sum': '$draw'}
                }
            }
        ])
        player_eco_stats_list = list(player_eco_stats)
        ecos = []
        for e in player_eco_stats_list:
            ecos.append(e['_id'])
    names = Players.objects.filter(Q(name__ne=name) & Q(elo__gte=elo - r) & Q(elo__lte=elo + r)).distinct("name")
    eco_stats = Games.objects.aggregate([
        {
            '$match': {'$and': [{'$or': [{'white': {'$in': names}}, {'black': {'$in': names}}]},
                                {'eco': {'$in': ecos}}]}
        },
        {
            '$project': {
                'eco': 1,
                'win': {'$cond': {'if': {'$or': [
                    {'$and': [{'$eq': ['$result', '1-0']}, {'$in': ['$white', names]}]},
                    {'$and': [{'$eq': ['$result', '0-1']}, {'$in': ['$black', names]}]}
                ]}, 'then': 1, 'else': 0}},
                'loss': {'$cond': {'if': {'$or': [
                    {'$and': [{'$eq': ['$result', '1-0']}, {'$in': ['$black', names]}]},
                    {'$and': [{'$eq': ['$result', '0-1']}, {'$in': ['$white', names]}]}
                ]}, 'then': 1, 'else': 0}},
                'draw': {'$cond': {'if': {'$and': [
                    {'$eq': ['$result', '1/2-1/2']},
                    {'$in': ['$black', names]},
                    {'$in': ['$white', names]}
                ]}, 'then': 2, 'else': {'$cond': {'if': {'$eq': ['$result', '1/2-1/2']}, 'then': 1, 'else': 0}}}}
            }
        },
        {
            '$group': {
                '_id': '$eco',
                'wins': {'$sum': '$win'},
                'losses': {'$sum': '$loss'},
                'draws': {'$sum': '$draw'}
            }
        }
    ])
    temp = list(eco_stats)
    for player_eco in player_eco_stats_list:
        win_percentage = round((player_eco['wins'] / (player_eco['wins'] + player_eco['losses'] + player_eco['draws']))
                               * 100, 2)
        loss_percentage = round((player_eco['losses'] / (player_eco['wins'] + player_eco['losses'] +
                                                         player_eco['draws'])) * 100, 2)
        draw_percentage = round((player_eco['draws'] / (player_eco['wins'] + player_eco['losses'] +
                                                        player_eco['draws'])) * 100, 2)
        for eco in temp:
            if player_eco['_id'] == eco['_id']:
                other_win_percentage = round((eco['wins'] / (eco['wins'] + eco['losses'] + eco['draws'])) * 100, 2)
                other_loss_percentage = round((eco['losses'] / (eco['wins'] + eco['losses'] + eco['draws'])) * 100, 2)
                other_draw_percentage = round((eco['draws'] / (eco['wins'] + eco['losses'] + eco['draws'])) * 100, 2)
                response[eco['_id']] = {'your wins': player_eco['wins'], 'other players wins': eco['wins'],
                                        'your win percentage': win_percentage,
                                        'other players win percentage': other_win_percentage,
                                        'your losses': player_eco['losses'], 'other players losses': eco['losses'],
                                        'your loss percentage': loss_percentage,
                                        'other players loss percentage': other_loss_percentage,
                                        'your draws': player_eco['draws'], 'other players draws': eco['draws'],
                                        'your draw percentage': draw_percentage,
                                        'other players draw percentage': other_draw_percentage}
        if player_eco['_id'] not in response.keys():
            response[player_eco['_id']] = {'your wins': player_eco['wins'], 'other players wins': 0,
                                           'your win percentage': win_percentage, 'other players win percentage': 0,
                                           'your losses': player_eco['losses'], 'other players losses': 0,
                                           'your loss percentage': loss_percentage, 'other players loss percentage': 0,
                                           'your draws': player_eco['draws'], 'other players draws': 0,
                                           'your draw percentage': draw_percentage, 'other players draw percentage': 0}
    return response


"""
def calculate_opening_comparisons(name, params):
    dictionary = {}
    compare_dictionary = {}
    r = 10
    elo = 0
    if "elo" in params.keys():
        elo = params["elo"]
    else:
        player = Players.objects.filter(Q(name=name)).first()
        if player:
            elo = player.elo
    if "range" in params.keys():
        r = params["range"]
    if "eco" in params.keys():
        ecos = params["eco"].split(",")
    else:
        ecos = []
        games = Games.objects.filter(Q(white=name) | Q(black=name))
        for game in games:
            if game.eco not in ecos:
                ecos.append(game.eco)
    players = Players.objects.filter(Q(name__ne=name) & Q(elo__gte=elo - r) & Q(elo__lte=elo + r))
    for player in players:
        for eco in ecos:
            if eco not in compare_dictionary.keys():
                compare_dictionary[eco] = {"compare_wins": 0, "compare_losses": 0, "compare_draws": 0}
            if eco in player.openings.keys():
                compare_dictionary[eco] = {"compare_wins": compare_dictionary[eco]["compare_wins"] +
                                                           player.openings[eco]["wins"],
                                           "compare_losses": compare_dictionary[eco]["compare_losses"] +
                                                             player.openings[eco]["losses"],
                                           "compare_draws": compare_dictionary[eco]["compare_draws"] +
                                                            player.openings[eco]["draws"]}
    games, white_games, black_games = database_query(name, params)
    temp_dictionary = filter_games(games, name, "eco")
    for eco in ecos:
        compare_win_percentages = 0.
        compare_loss_percentages = 0.
        compare_draw_percentages = 0.
        if compare_dictionary[eco]["compare_wins"] + compare_dictionary[eco]["compare_losses"] + \
                compare_dictionary[eco]["compare_draws"] != 0:
            compare_win_percentages = round((compare_dictionary[eco]["compare_wins"] /
                                             (compare_dictionary[eco]["compare_wins"] +
                                              compare_dictionary[eco]["compare_losses"] +
                                              compare_dictionary[eco]["compare_draws"])) * 100, 2)
            compare_loss_percentages = round((compare_dictionary[eco]["compare_losses"] /
                                              (compare_dictionary[eco]["compare_wins"] +
                                               compare_dictionary[eco]["compare_losses"] +
                                               compare_dictionary[eco]["compare_draws"])) * 100, 2)
            compare_draw_percentages = round((compare_dictionary[eco]["compare_draws"] /
                                              (compare_dictionary[eco]["compare_wins"] +
                                               compare_dictionary[eco]["compare_losses"] +
                                               compare_dictionary[eco]["compare_draws"])) * 100, 2)
        dictionary[eco] = {"your wins": temp_dictionary[eco]["won_games"],
                           "other players wins": compare_dictionary[eco]["compare_wins"],
                           "your losses": temp_dictionary[eco]["lost_games"],
                           "other players losses": compare_dictionary[eco]["compare_losses"],
                           "your draws": temp_dictionary[eco]["drawn_games"],
                           "other players draws": compare_dictionary[eco]["compare_draws"],
                           "your win percentages": temp_dictionary[eco]["percentage_won"],
                           "other players win percentages": compare_win_percentages,
                           "your loss percentages": temp_dictionary[eco]["percentage_lost"],
                           "other players loss percentages": compare_loss_percentages,
                           "your draw percentages": temp_dictionary[eco]["percentage_drawn"],
                           "other players draw percentages": compare_draw_percentages}
    return dictionary
"""
