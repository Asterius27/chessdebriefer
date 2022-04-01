from mongoengine import Q
from ChessDebriefer.Logic.percentages import create_side_percentages_dictionary, create_percentages_dictionary, \
    calculate_wdl_percentages
from ChessDebriefer.models import Games


def calculate_percentages_comparisons(name, params):
    response = {}
    elo, r = check_params_comparisons(name, params)
    temp = {'minelo': str(elo - r), 'maxelo': str(elo + r)}
    white_percentages = create_side_percentages_dictionary(name, temp, True, '', '')
    black_percentages = create_side_percentages_dictionary(name, temp, False, '', '')
    side_percentages = {'white': white_percentages['white'], 'black': black_percentages['black']}
    # names = Players.objects.filter(Q(name__ne=name) & Q(elo__gte=elo - r) & Q(elo__lte=elo + r)).distinct("name")
    other_players_white_percentages = create_other_players_side_percentages_dictionary(name, elo, r, True)
    other_players_black_percentages = create_other_players_side_percentages_dictionary(name, elo, r, False)
    side_percentages['white'].update(other_players_white_percentages['white'])
    side_percentages['black'].update(other_players_black_percentages['black'])
    response['general percentages'] = {'your wins': side_percentages['white']['your wins'] +
                                                    side_percentages['black']['your wins'],
                                       'your losses': side_percentages['white']['your losses'] +
                                                      side_percentages['black']['your losses'],
                                       'your draws': side_percentages['white']['your draws'] +
                                                     side_percentages['black']['your draws'],
                                       'your win percentage': 0., 'your loss percentage': 0.,
                                       'your draw percentage': 0.,
                                       'other players wins': side_percentages['white']['other players wins'] +
                                                             side_percentages['black']['other players wins'],
                                       'other players losses': side_percentages['white']['other players losses'] +
                                                               side_percentages['black']['other players losses'],
                                       'other players draws': side_percentages['white']['other players draws'] +
                                                              side_percentages['black']['other players draws'],
                                       'other players win percentage': 0., 'other players loss percentage': 0.,
                                       'other players draw percentage': 0.}
    response['general percentages']['your win percentage'] = round((response['general percentages']['your wins'] /
        (response['general percentages']['your wins'] + response['general percentages']['your losses'] +
         response['general percentages']['your draws'])) * 100, 2)
    response['general percentages']['your loss percentage'] = round((response['general percentages']['your losses'] /
        (response['general percentages']['your wins'] + response['general percentages']['your losses'] +
         response['general percentages']['your draws'])) * 100, 2)
    response['general percentages']['your draw percentage'] = round((response['general percentages']['your draws'] /
        (response['general percentages']['your wins'] + response['general percentages']['your losses'] +
         response['general percentages']['your draws'])) * 100, 2)
    response['general percentages']['other players win percentage'] = round(
        (response['general percentages']['other players wins'] / (response['general percentages']['other players wins']
         + response['general percentages']['other players losses'] +
         response['general percentages']['other players draws'])) * 100, 2)
    response['general percentages']['other players loss percentage'] = round(
        (response['general percentages']['other players losses'] /
         (response['general percentages']['other players wins'] +
          response['general percentages']['other players losses'] +
          response['general percentages']['other players draws'])) * 100, 2)
    response['general percentages']['other players draw percentage'] = round(
        (response['general percentages']['other players draws'] / (response['general percentages']['other players wins']
         + response['general percentages']['other players losses'] +
         response['general percentages']['other players draws'])) * 100, 2)
    response['side percentages'] = {'white': side_percentages['white'], 'black': side_percentages['black']}
    return response


def calculate_event_comparisons(name, params):
    elo, r = check_params_comparisons(name, params)
    player_event_stats, events = calculate_player_stats(name, elo, r, params, 'event')
    # names = Players.objects.filter(Q(name__ne=name) & Q(elo__gte=elo - r) & Q(elo__lte=elo + r)).distinct("name")
    event_stats = create_other_players_percentages_dictionary(name, elo, r, 'event', events)
    return create_response(player_event_stats, event_stats)


def calculate_termination_comparisons(name, params):
    elo, r = check_params_comparisons(name, params)
    player_termination_stats, terminations = calculate_player_stats(name, elo, r, params, 'termination')
    # names = Players.objects.filter(Q(name__ne=name) & Q(elo__gte=elo - r) & Q(elo__lte=elo + r)).distinct("name")
    termination_stats = create_other_players_percentages_dictionary(name, elo, r, 'termination', terminations)
    return create_response(player_termination_stats, termination_stats)


def calculate_opening_comparisons(name, params):
    elo, r = check_params_comparisons(name, params)
    player_eco_stats, ecos = calculate_player_stats(name, elo, r, params, 'eco')
    # names = Players.objects.filter(Q(name__ne=name) & Q(elo__gte=elo - r) & Q(elo__lte=elo + r)).distinct("name")
    eco_stats = create_other_players_percentages_dictionary(name, elo, r, 'eco', ecos)
    return create_response(player_eco_stats, eco_stats)


def create_response(your_stats, other_players_stats):
    response = {}
    for key in your_stats:
        if key in other_players_stats.keys():
            response[key] = your_stats[key]
            response[key].update(other_players_stats[key])
        if key not in response.keys():
            response[key] = your_stats[key]
            response[key].update({'other players wins': 0, 'other players win percentage': 0, 'other players losses': 0,
                                  'other players loss percentage': 0, 'other players draws': 0,
                                  'other players draw percentage': 0})
    return response


def calculate_player_stats(name, elo, r, params, specific):
    temp = {'minelo': str(elo - r), 'maxelo': str(elo + r)}
    if specific in params.keys():
        specifics = params[specific].split(",")
        player_stats = create_percentages_dictionary(name, temp, specific, specifics)
    else:
        player_stats = create_percentages_dictionary(name, temp, specific, [])
        specifics = []
        for key in player_stats:
            specifics.append(key)
    return player_stats, specifics


def create_other_players_side_percentages_dictionary(name, elo, r, side):
    dictionary = {}
    if side:
        player = 'white'
        player_elo = 'white_elo'
        win = '1-0'
        loss = '0-1'
    else:
        player = 'black'
        player_elo = 'black_elo'
        win = '0-1'
        loss = '1-0'
    other_players_percentages = Games.objects.aggregate([
        {
            '$match': {'$and': [{player: {'$ne': name}}, {player_elo: {'$gte': elo - r, '$lte': elo + r}}]}
        },
        {
            '$project': {
                'win': {'$cond': {'if': {'$eq': ['$result', win]}, 'then': 1, 'else': 0}},
                'loss': {'$cond': {'if': {'$eq': ['$result', loss]}, 'then': 1, 'else': 0}},
                'draw': {'$cond': {'if': {'$eq': ['$result', '1/2-1/2']}, 'then': 1, 'else': 0}}
            }
        },
        {
            '$group': {
                '_id': 'null',
                'wins': {'$sum': '$win'},
                'losses': {'$sum': '$loss'},
                'draws': {'$sum': '$draw'}
            }
        }
    ])
    for s in other_players_percentages:
        percentage_won, percentage_lost, percentage_drawn = calculate_wdl_percentages(s['wins'], s['losses'],
                                                                                      s['draws'])
        dictionary[player] = {'other players wins': s['wins'], 'other players losses': s['losses'],
                              'other players draws': s['draws'], 'other players win percentage': percentage_won,
                              'other players loss percentage': percentage_lost,
                              'other players draw percentage': percentage_drawn}
    return dictionary


def create_other_players_percentages_dictionary(name, elo, r, group, specific):
    dictionary = {}
    dollar_group = '$' + group
    games_stats = Games.objects.aggregate([
        {
            '$match': {'$and': [{'$or': [{'$and': [{'white': {'$ne': name}},
                                                   {'white_elo': {'$gte': elo - r, '$lte': elo + r}}]},
                                         {'$and': [{'black': {'$ne': name}},
                                                   {'black_elo': {'$gte': elo - r, '$lte': elo + r}}]}]},
                                {group: {'$in': specific}}]}
        },
        {
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
        },
        {
            '$group': {
                '_id': dollar_group,
                'wins': {'$sum': '$win'},
                'losses': {'$sum': '$loss'},
                'draws': {'$sum': '$draw'}
            }
        }
    ])
    for g in games_stats:
        percentage_won, percentage_lost, percentage_drawn = calculate_wdl_percentages(g['wins'], g['losses'],
                                                                                      g['draws'])
        dictionary[g['_id']] = {'other players wins': g['wins'], 'other players losses': g['losses'],
                                'other players draws': g['draws'], 'other players win percentage': percentage_won,
                                'other players loss percentage': percentage_lost,
                                'other players draw percentage': percentage_drawn}
    return dictionary


'''DEPRECATED: too slow (20 seconds more or less)
def find_players(name, elo, r):
    players = Games.objects.aggregate([
        {
            '$sort': {'date': -1}
        },
        {
            '$group': {
                '_id': '$white',
                'elo': {'$first': '$white_elo'},
                'date': {'$first': '$date'}
            }
        },
        {
            '$lookup': {
                'from': 'games',
                'let': {'player': '$_id', 'white_date': '$date'},
                'pipeline': [
                    {'$sort': {'date': -1}},
                    {'$group': {
                        '_id': '$black',
                        'new_elo': {'$first': '$black_elo'},
                        'date': {'$first': '$date'}
                    }},
                    {'$match': {'$expr': {'$and': [
                        {'$eq': ['$_id', '$$player']},
                        {'$gt': ['$date', '$$white_date']}
                    ]}}},
                    {'$project': {'_id': 0, 'date': 0}}
                ],
                'as': 'arr'
            }
        },
        {
            '$replaceRoot': {'newRoot': {'$mergeObjects': [{'$arrayElemAt': ['$arr', 0]}, '$$ROOT']}}
        },
        {
            '$project': {
                '_id': 1,
                'elo': {'$ifNull': ['$new_elo', '$elo']}
            }
        },
        {
            '$match': {
                '$and': [{'_id': {'$ne': name}}, {'elo': {'$gte': elo - r, '$lte': elo + r}}]
            }
        },
        {
            '$group': {
                '_id': 'null',
                'names': {'$push': '$_id'}
            }
        }
    ])
    names = []
    for player in players:
        names = player['names']
    return names
'''


def check_params_comparisons(name, params):
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
    return elo, r
