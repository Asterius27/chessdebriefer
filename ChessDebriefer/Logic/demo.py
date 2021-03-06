from ChessDebriefer.Logic.compare import check_params_comparisons, create_other_players_percentages_dictionary
from ChessDebriefer.Logic.percentages import check_params, calculate_wdl_percentages
from ChessDebriefer.models import Games


def calculate_openings_best_worst(name, params):
    response = {}
    ecos = []
    response['best'] = create_percentages_dictionary(name, params, -1, 'eco')
    response['worst'] = create_percentages_dictionary(name, params, 1, 'eco')
    for key in response['best']:
        ecos.append(key)
    for key in response['worst']:
        if key not in ecos:
            ecos.append(key)
    elo, r = check_params_comparisons(name, params)
    eco_stats = create_other_players_percentages_dictionary(name, elo, r, 'eco', ecos)
    for key in eco_stats:
        if key in response['best'].keys():
            response['best'][key].update(eco_stats[key])
        if key in response['worst'].keys():
            response['worst'][key].update(eco_stats[key])
    return response


def calculate_openings_best_worst_simplified(name, params):
    best = []
    worst = []
    others_best = []
    others_worst = []
    best_dict = create_percentages_dictionary(name, params, -1, 'eco')
    worst_dict = create_percentages_dictionary(name, params, 1, 'eco')
    for key in best_dict:
        best.append(key)
    for key in worst_dict:
        worst.append(key)
    elo, r = check_params_comparisons(name, params)
    others_best_dict = create_players_percentages_dictionary(name, elo, r, params, -1, 'eco')
    others_worst_dict = create_players_percentages_dictionary(name, elo, r, params, 1, 'eco')
    for key in others_best_dict:
        others_best.append(key)
    for key in others_worst_dict:
        others_worst.append(key)
    response = {'your best': best, 'your worst': worst, 'other players best': others_best,
                'other players worst': others_worst}
    return response


def create_percentages_dictionary(name, params, order, group):
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
    if opponent:
        match_query = {
            '$match': {'$and': [
                {'$or': [{'$and': [{'white': name}, {'black': opponent},
                                   {'white_elo': {'$gt': min_elo, '$lt': max_elo}}]},
                         {'$and': [{'black': name}, {'white': opponent},
                                   {'black_elo': {'$gt': min_elo, '$lt': max_elo}}]}]},
                {'date': {'$gt': from_date, '$lt': to_date}}
            ]}
        }
    else:
        match_query = {
            '$match': {'$and': [
                {'$or': [{'$and': [{'white': name}, {'white_elo': {'$gt': min_elo, '$lt': max_elo}}]},
                         {'$and': [{'black': name}, {'black_elo': {'$gt': min_elo, '$lt': max_elo}}]}]},
                {'date': {'$gt': from_date, '$lt': to_date}}
            ]}
        }
    return general_query(params, order, group, match_query, project_query)


def create_players_percentages_dictionary(name, elo, r, params, order, group):
    project_query = {
        '$project': {
            group: 1,
            'win': {'$cond': {'if': {'$or': [
                {'$and': [{'$eq': ['$result', '1-0']},
                          {'$and': [{'$ne': ['$white', name]},
                                    {'$gte': ['$white_elo', elo - r]}, {'$lte': ['$white_elo', elo + r]}]}]},
                {'$and': [{'$eq': ['$result', '0-1']},
                          {'$and': [{'$ne': ['$black', name]},
                                    {'$gte': ['$black_elo', elo - r]}, {'$lte': ['$black_elo', elo + r]}]}]}
            ]}, 'then': 1, 'else': 0}},
            'loss': {'$cond': {'if': {'$or': [
                {'$and': [{'$eq': ['$result', '1-0']},
                          {'$and': [{'$ne': ['$black', name]},
                                    {'$gte': ['$black_elo', elo - r]}, {'$lte': ['$black_elo', elo + r]}]}]},
                {'$and': [{'$eq': ['$result', '0-1']},
                          {'$and': [{'$ne': ['$white', name]},
                                    {'$gte': ['$white_elo', elo - r]}, {'$lte': ['$white_elo', elo + r]}]}]}
            ]}, 'then': 1, 'else': 0}},
            'draw': {'$cond': {'if': {'$and': [
                {'$eq': ['$result', '1/2-1/2']},
                {'$and': [{'$ne': ['$white', name]}, {'$gte': ['$white_elo', elo - r]},
                          {'$lte': ['$white_elo', elo + r]}]},
                {'$and': [{'$ne': ['$black', name]}, {'$gte': ['$black_elo', elo - r]},
                          {'$lte': ['$black_elo', elo + r]}]}
            ]}, 'then': 2, 'else': {'$cond': {'if': {'$eq': ['$result', '1/2-1/2']}, 'then': 1, 'else': 0}}}}
        }
    }
    match_query = {
        '$match': {'$and': [{'$or': [{'$and': [{'white': {'$ne': name}},
                                               {'white_elo': {'$gte': elo - r, '$lte': elo + r}}]},
                                     {'$and': [{'black': {'$ne': name}},
                                               {'black_elo': {'$gte': elo - r, '$lte': elo + r}}]}]}]}
    }
    return general_query(params, order, group, match_query, project_query)


def general_query(params, order, group, match, project):
    dollar_group = '$' + group
    dictionary = {}
    if "min_played" in params.keys():
        min_played = int(params["min_played"])
    else:
        min_played = 10
    if "limit" in params.keys():
        limit = int(params["limit"])
    else:
        limit = 3
    group_query = {
        '$group': {
            '_id': dollar_group,
            'wins': {'$sum': '$win'},
            'losses': {'$sum': '$loss'},
            'draws': {'$sum': '$draw'}
        }
    }
    project_query = {
        '$project': {
            '_id': 1,
            'wins': 1,
            'losses': 1,
            'draws': 1,
            'matches': {'$add': ['$wins', '$losses', '$draws']},
            'win_percentage': {'$multiply': [{'$divide': ['$wins', {'$add': ['$wins', '$losses', '$draws']}]}, 100]}
        }
    }
    having_query = {'$match': {'matches': {'$gte': min_played}}}
    sort_query = {'$sort': {'win_percentage': order}}
    limit_query = {'$limit': limit}
    games_stats = Games.objects.aggregate([match, project, group_query, project_query, having_query, sort_query,
                                           limit_query])
    for g in games_stats:
        percentage_won, percentage_lost, percentage_drawn = calculate_wdl_percentages(g['wins'], g['losses'],
                                                                                      g['draws'])
        dictionary[g['_id']] = {'your wins': g['wins'], 'your losses': g['losses'], 'your draws': g['draws'],
                                'your win percentage': percentage_won, 'your loss percentage': percentage_lost,
                                'your draw percentage': percentage_drawn}
    return dictionary
