import datetime
import re
from ChessDebriefer.models import Games


# TODO add throw comeback percentages
def calculate_percentages_database(name, params):
    response = {}
    white = create_side_percentages_dictionary(name, params, True)
    black = create_side_percentages_dictionary(name, params, False)
    side_percentages = {'white': white['white'], 'black': black['black']}
    response['general percentages'] = {'your wins': side_percentages['white']['your wins'] +
                                                    side_percentages['black']['your wins'],
                                       'your losses': side_percentages['white']['your losses'] +
                                                      side_percentages['black']['your losses'],
                                       'your draws': side_percentages['white']['your draws'] +
                                                     side_percentages['black']['your draws']}
    response['general percentages']['your win percentage'] = \
        round((response['general percentages']['your wins'] / (response['general percentages']['your wins'] +
              response['general percentages']['your losses'] + response['general percentages']['your draws'])) * 100, 2)
    response['general percentages']['your loss percentage'] = \
        round((response['general percentages']['your losses'] / (response['general percentages']['your wins'] +
              response['general percentages']['your losses'] + response['general percentages']['your draws'])) * 100, 2)
    response['general percentages']['your draw percentage'] = \
        round((response['general percentages']['your draws'] / (response['general percentages']['your wins'] +
              response['general percentages']['your losses'] + response['general percentages']['your draws'])) * 100, 2)
    response['side percentages'] = side_percentages
    response['throw comeback percentages'] = {}
    return response


def calculate_event_percentages_database(name, params):
    return create_percentages_dictionary(name, params, 'event', [])


# TODO add management of eco param
def calculate_opening_percentages_database(name, params):
    if "eco" not in params.keys():
        return create_percentages_dictionary(name, params, 'eco', [])
    else:
        ecos = params["ecos"].split(",")
        return create_percentages_dictionary(name, params, 'eco', ecos)


def calculate_termination_percentages_database(name, params):
    return create_percentages_dictionary(name, params, 'termination', [])


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
        if g['wins'] + g['losses'] + g['draws'] != 0:
            percentage_won = round((g['wins'] / (g['wins'] + g['losses'] + g['draws'])) * 100, 2)
            percentage_lost = round((g['losses'] / (g['wins'] + g['losses'] + g['draws'])) * 100, 2)
            percentage_drawn = round((g['draws'] / (g['wins'] + g['losses'] + g['draws'])) * 100, 2)
        else:
            percentage_won = 0.
            percentage_lost = 0.
            percentage_drawn = 0.
        dictionary[g['_id']] = {'your wins': g['wins'], 'your losses': g['losses'], 'your draws': g['draws'],
                                'your win percentage': percentage_won, 'your loss percentage': percentage_lost,
                                'your draw percentage': percentage_drawn}
    return dictionary


def create_side_percentages_dictionary(name, params, side):
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
        player_percentages = Games.objects.aggregate([
            {
                '$match': {'$and': [{player: name}, {player_elo: {'$gt': min_elo, '$lt': max_elo}},
                                    {'date': {'$gt': from_date, '$lt': to_date}}]}
            },
            project_query,
            group_query
        ])
    for s in player_percentages:
        percentage_won = round((s['wins'] / (s['wins'] + s['losses'] + s['draws'])) * 100, 2)
        percentage_lost = round((s['losses'] / (s['wins'] + s['losses'] + s['draws'])) * 100, 2)
        percentage_drawn = round((s['draws'] / (s['wins'] + s['losses'] + s['draws'])) * 100, 2)
        dictionary[player] = {'your wins': s['wins'], 'your losses': s['losses'], 'your draws': s['draws'],
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
