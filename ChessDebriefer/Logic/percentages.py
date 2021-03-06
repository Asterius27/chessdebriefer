import datetime
import re
from mongoengine import Q
from ChessDebriefer.Logic.games import average_game_centipawn
from ChessDebriefer.models import Games


def calculate_percentages_database(name, params):
    response = {}
    white = create_side_percentages_dictionary(name, params, True, '', '')
    black = create_side_percentages_dictionary(name, params, False, '', '')
    if not white:
        white = {'white': {"your wins": 0, "your losses": 0, "your draws": 0, "your win percentage": 0.,
                           "your loss percentage": 0., "your draw percentage": 0.}}
    if not black:
        black = {'black': {"your wins": 0, "your losses": 0, "your draws": 0, "your win percentage": 0.,
                           "your loss percentage": 0., "your draw percentage": 0.}}
    side_percentages = {'white': white['white'], 'black': black['black']}
    response['general percentages'] = {'your wins': side_percentages['white']['your wins'] +
                                                    side_percentages['black']['your wins'],
                                       'your losses': side_percentages['white']['your losses'] +
                                                      side_percentages['black']['your losses'],
                                       'your draws': side_percentages['white']['your draws'] +
                                                     side_percentages['black']['your draws']}
    percentage_won, percentage_lost, percentage_drawn = calculate_wdl_percentages(
        response['general percentages']['your wins'], response['general percentages']['your losses'],
        response['general percentages']['your draws'])
    response['general percentages']['your win percentage'] = percentage_won
    response['general percentages']['your loss percentage'] = percentage_lost
    response['general percentages']['your draw percentage'] = percentage_drawn
    response['side percentages'] = side_percentages
    return response


def calculate_event_percentages_database(name, params):
    return create_percentages_dictionary(name, params, 'event', [])


def calculate_opening_percentages_database(name, params):
    if "eco" not in params.keys():
        return create_percentages_dictionary(name, params, 'eco', [])
    else:
        response = {}
        if "-" in params["eco"]:
            boundaries = params["eco"].split("-")
            ecos = calculate_ecos_list(boundaries)
        else:
            ecos = params["eco"].split(",")
        variations_dictionary = eco_variations_query(name, params, ecos)
        general_dictionary = create_percentages_dictionary(name, params, 'eco', ecos)
        for eco in ecos:
            if eco in variations_dictionary.keys() and eco in general_dictionary.keys():
                response[eco] = {}
                response[eco]["general stats"] = general_dictionary[eco]
                response[eco]["side stats"] = {}
                response[eco]["side stats"]["white"] = create_side_percentages_dictionary(name, params, True, 'eco',
                                                                                          eco)
                response[eco]["side stats"]["black"] = create_side_percentages_dictionary(name, params, False, 'eco',
                                                                                          eco)
                response[eco]["variations stats"] = variations_dictionary[eco]
        return response


def calculate_termination_percentages_database(name, params):
    return create_percentages_dictionary(name, params, 'termination', [])


def calculate_throws_comebacks(name, params):
    from_date, to_date, min_elo, max_elo, opponent = check_params(params)
    if "opponent" not in params.keys():
        games = Games.objects.filter(((Q(white=name) & Q(white_elo__gte=min_elo) & Q(white_elo__lte=max_elo)) |
                                      (Q(black=name) & Q(black_elo__gte=min_elo) & Q(black_elo__lte=max_elo)))
                                     & Q(date__gte=from_date) & Q(date__lte=to_date))
    else:
        games = Games.objects.filter(((Q(white=name) & Q(black=params["opponent"]) & Q(white_elo__gte=min_elo) &
                                       Q(white_elo__lte=max_elo)) | (Q(black=name) & Q(white=params["opponent"]) &
                                                                     Q(black_elo__gte=min_elo) &
                                                                     Q(black_elo__lte=max_elo))) &
                                     Q(date__gte=from_date) & Q(date__lte=to_date))
    return filter_throws_comebacks(games, name)


def create_percentages_dictionary(name, params, group, specific):
    dollar_group = '$' + group
    dictionary = {}
    from_date, to_date, min_elo, max_elo, opponent = check_params(params)
    project_query = {
        '$project': {
            group: 1,
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
    }
    group_query = {
        '$group': {
            '_id': dollar_group,
            'wins': {'$sum': '$win'},
            'losses': {'$sum': '$loss'},
            'draws': {'$sum': '$draw'}
        }
    }
    if opponent:
        if specific:
            games_stats = Games.objects.aggregate([
                {
                    '$match': {'$and': [
                        {'$or': [{'$and': [{'white': name}, {'black': opponent},
                                           {'white_elo': {'$gt': min_elo, '$lt': max_elo}}]},
                                 {'$and': [{'black': name}, {'white': opponent},
                                           {'black_elo': {'$gt': min_elo, '$lt': max_elo}}]}]},
                        {'date': {'$gt': from_date, '$lt': to_date}},
                        {group: {'$in': specific}}
                    ]}
                },
                project_query,
                group_query
            ])
        else:
            games_stats = Games.objects.aggregate([
                {
                    '$match': {'$and': [
                        {'$or': [{'$and': [{'white': name}, {'black': opponent},
                                           {'white_elo': {'$gt': min_elo, '$lt': max_elo}}]},
                                 {'$and': [{'black': name}, {'white': opponent},
                                           {'black_elo': {'$gt': min_elo, '$lt': max_elo}}]}]},
                        {'date': {'$gt': from_date, '$lt': to_date}}
                    ]}
                },
                project_query,
                group_query
            ])
    else:
        if specific:
            games_stats = Games.objects.aggregate([
                {
                    '$match': {'$and': [
                        {'$or': [{'$and': [{'white': name}, {'white_elo': {'$gt': min_elo, '$lt': max_elo}}]},
                                 {'$and': [{'black': name}, {'black_elo': {'$gt': min_elo, '$lt': max_elo}}]}]},
                        {'date': {'$gt': from_date, '$lt': to_date}},
                        {group: {'$in': specific}}
                    ]}
                },
                project_query,
                group_query
            ])
        else:
            games_stats = Games.objects.aggregate([
                {
                    '$match': {'$and': [
                        {'$or': [{'$and': [{'white': name}, {'white_elo': {'$gt': min_elo, '$lt': max_elo}}]},
                                 {'$and': [{'black': name}, {'black_elo': {'$gt': min_elo, '$lt': max_elo}}]}]},
                        {'date': {'$gt': from_date, '$lt': to_date}}
                    ]}
                },
                project_query,
                group_query
            ])
    for g in games_stats:
        percentage_won, percentage_lost, percentage_drawn = calculate_wdl_percentages(g['wins'], g['losses'],
                                                                                      g['draws'])
        dictionary[g['_id']] = {'your wins': g['wins'], 'your losses': g['losses'], 'your draws': g['draws'],
                                'your win percentage': percentage_won, 'your loss percentage': percentage_lost,
                                'your draw percentage': percentage_drawn}
    return dictionary


def create_side_percentages_dictionary(name, params, side, select, specific):
    dictionary = {}
    from_date, to_date, min_elo, max_elo, opponent = check_params(params)
    if side:
        player = 'white'
        player_opponent = 'black'
        player_elo = 'white_elo'
        win = '1-0'
        loss = '0-1'
    else:
        player = 'black'
        player_opponent = 'white'
        player_elo = 'black_elo'
        win = '0-1'
        loss = '1-0'
    project_query = {
        '$project': {
            'win': {'$cond': {'if': {'$eq': ['$result', win]}, 'then': 1, 'else': 0}},
            'loss': {'$cond': {'if': {'$eq': ['$result', loss]}, 'then': 1, 'else': 0}},
            'draw': {'$cond': {'if': {'$eq': ['$result', '1/2-1/2']}, 'then': 1, 'else': 0}}
        }
    }
    group_query = {
        '$group': {
            '_id': 'null',
            'wins': {'$sum': '$win'},
            'losses': {'$sum': '$loss'},
            'draws': {'$sum': '$draw'}
        }
    }
    if opponent:
        if specific and select:
            player_percentages = Games.objects.aggregate([
                {
                    '$match': {'$and': [{player: name}, {player_opponent: opponent},
                                        {player_elo: {'$gt': min_elo, '$lt': max_elo}},
                                        {'date': {'$gt': from_date, '$lt': to_date}}, {select: specific}]}
                },
                project_query,
                group_query
            ])
        else:
            player_percentages = Games.objects.aggregate([
                {
                    '$match': {'$and': [{player: name}, {player_opponent: opponent},
                                        {player_elo: {'$gt': min_elo, '$lt': max_elo}},
                                        {'date': {'$gt': from_date, '$lt': to_date}}]}
                },
                project_query,
                group_query
            ])
    else:
        if specific and select:
            player_percentages = Games.objects.aggregate([
                {
                    '$match': {'$and': [{player: name}, {player_elo: {'$gt': min_elo, '$lt': max_elo}},
                                        {'date': {'$gt': from_date, '$lt': to_date}}, {select: specific}]}
                },
                project_query,
                group_query
            ])
        else:
            player_percentages = Games.objects.aggregate([
                {
                    '$match': {'$and': [{player: name}, {player_elo: {'$gt': min_elo, '$lt': max_elo}},
                                        {'date': {'$gt': from_date, '$lt': to_date}}]}
                },
                project_query,
                group_query
            ])
    for s in player_percentages:
        percentage_won, percentage_lost, percentage_drawn = calculate_wdl_percentages(s['wins'], s['losses'],
                                                                                      s['draws'])
        dictionary[player] = {'your wins': s['wins'], 'your losses': s['losses'], 'your draws': s['draws'],
                              'your win percentage': percentage_won, 'your loss percentage': percentage_lost,
                              'your draw percentage': percentage_drawn}
    return dictionary


def eco_variations_query(name, params, ecos):
    dictionary = {}
    from_date, to_date, min_elo, max_elo, opponent = check_params(params)
    if opponent:
        match_query = {
            '$match': {'$and': [
                {'$or': [{'$and': [{'white': name}, {'black': opponent},
                                   {'white_elo': {'$gt': min_elo, '$lt': max_elo}}]},
                         {'$and': [{'black': name}, {'white': opponent},
                                   {'black_elo': {'$gt': min_elo, '$lt': max_elo}}]}]},
                {'date': {'$gt': from_date, '$lt': to_date}},
                {'eco': {'$in': ecos}}
            ]}
        }
    else:
        match_query = {
            '$match': {'$and': [
                {'$or': [{'$and': [{'white': name}, {'white_elo': {'$gt': min_elo, '$lt': max_elo}}]},
                         {'$and': [{'black': name}, {'black_elo': {'$gt': min_elo, '$lt': max_elo}}]}]},
                {'date': {'$gt': from_date, '$lt': to_date}},
                {'eco': {'$in': ecos}}
            ]}
        }
    variation_percentages = Games.objects.aggregate([
        match_query,
        {
            '$lookup': {
                'from': 'openings',
                'let': {'op': '$opening_id'},
                'pipeline': [
                    {'$match': {'$expr': {'$eq': ['$_id', '$$op']}}},
                    {'$project': {'_id': 0, 'eco': 0, 'moves': 0, 'engine_evaluation': 0}}
                ],
                'as': 'opening_name'
            }
        },
        {
            '$replaceRoot': {'newRoot': {'$mergeObjects': [{'$arrayElemAt': ['$opening_name', 0]}, '$$ROOT']}}
        },
        {
            '$project': {
                'eco': 1,
                'opening_id': 1,
                'white_opening': 1,
                'black_opening': 1,
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
                '_id': '$opening_id',
                'eco': {'$first': '$eco'},
                'white_opening': {'$first': '$white_opening'},
                'black_opening': {'$first': '$black_opening'},
                'wins': {'$sum': '$win'},
                'losses': {'$sum': '$loss'},
                'draws': {'$sum': '$draw'}
            }
        }
    ])
    i = 0
    for s in variation_percentages:
        if s['eco'] not in dictionary.keys():
            dictionary[s['eco']] = {}
        percentage_won, percentage_lost, percentage_drawn = calculate_wdl_percentages(s['wins'], s['losses'],
                                                                                      s['draws'])
        if s['black_opening'] != '?':
            key = s['white_opening'] + " " + s['black_opening']
        else:
            key = s['white_opening']
        if key in dictionary[s['eco']].keys():
            key = key + " " + str(i)
            i += 1
        dictionary[s['eco']][key] = {'your wins': s['wins'], 'your losses': s['losses'], 'your draws': s['draws'],
                                     'your win percentage': percentage_won, 'your loss percentage': percentage_lost,
                                     'your draw percentage': percentage_drawn}
    return dictionary


def check_params(params):
    date_pattern = re.compile(r'^\d{4}-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])$')
    elo_pattern = re.compile(r'^\d{1,4}$')
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
        opponent = ""
    else:
        opponent = params["opponent"]
    return from_date, to_date, min_elo, max_elo, opponent


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


# upper bound is excluded
def calculate_ecos_list(boundaries):
    ecos = []
    letter = boundaries[0][0]
    number = int(boundaries[0][1] + boundaries[0][2])
    while letter + new_str(number) != boundaries[1]:
        ecos.append(letter + new_str(number))
        if number < 99:
            number += 1
        else:
            number = 0
            letter = chr(ord(letter) + 1)
    print(ecos)
    return ecos


def new_str(n):
    if n < 10:
        return "0" + str(n)
    else:
        return str(n)


def calculate_wdl_percentages(wins, losses, draws):
    if wins + losses + draws != 0:
        percentage_won = round((wins / (wins + losses + draws)) * 100, 2)
        percentage_lost = round((losses / (wins + losses + draws)) * 100, 2)
        percentage_drawn = round((draws / (wins + losses + draws)) * 100, 2)
        return percentage_won, percentage_lost, percentage_drawn
    else:
        return 0., 0., 0.
