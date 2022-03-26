from mongoengine import Q
from ChessDebriefer.Logic.compare import check_params_comparisons, create_other_players_percentages_dictionary
from ChessDebriefer.Logic.percentages_database import check_params
from ChessDebriefer.models import Games, Players

# TODO update readme


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
    names = Players.objects.filter(Q(name__ne=name) & Q(elo__gte=elo - r) & Q(elo__lte=elo + r)).distinct("name")
    eco_stats = create_other_players_percentages_dictionary(names, {}, 'eco', ecos)
    for key in eco_stats:
        if key in response['best'].keys():
            response['best'][key].update(eco_stats[key])
        if key in response['worst'].keys():
            response['worst'][key].update(eco_stats[key])
    return response


def create_percentages_dictionary(name, params, order, group):
    dollar_group = '$' + group
    dictionary = {}
    from_date, to_date, min_elo, max_elo, opponent = check_params(params)
    if "min_played" in params.keys():
        min_played = params["min_played"]
    else:
        min_played = 10
    if "limit" in params.keys():
        limit = params["limit"]
    else:
        limit = 3
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
    project_query_2 = {
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
    if opponent:
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
            project_query, group_query, project_query_2, having_query, sort_query, limit_query
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
            project_query, group_query, project_query_2, having_query, sort_query, limit_query
        ])
    for g in games_stats:
        percentage_won = round((g['wins'] / (g['wins'] + g['losses'] + g['draws'])) * 100, 2)
        percentage_lost = round((g['losses'] / (g['wins'] + g['losses'] + g['draws'])) * 100, 2)
        percentage_drawn = round((g['draws'] / (g['wins'] + g['losses'] + g['draws'])) * 100, 2)
        dictionary[g['_id']] = {'your wins': g['wins'], 'your losses': g['losses'], 'your draws': g['draws'],
                                'your win percentage': percentage_won, 'your loss percentage': percentage_lost,
                                'your draw percentage': percentage_drawn}
    return dictionary
