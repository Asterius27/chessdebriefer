from mongoengine import Q
from ChessDebriefer.models import Games, Players


# TODO add percentages to response
def calculate_percentages_comparisons(name, params):
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
    player_white_percentages = Games.objects.aggregate([
        {
            '$match': {'white': name}
        },
        {
            '$project': {
                'win': {'$cond': {'if': {'$eq': ['$result', '1-0']}, 'then': 1, 'else': 0}},
                'loss': {'$cond': {'if': {'$eq': ['$result', '0-1']}, 'then': 1, 'else': 0}},
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
    player_black_percentages = Games.objects.aggregate([
        {
            '$match': {'black': name}
        },
        {
            '$project': {
                'win': {'$cond': {'if': {'$eq': ['$result', '0-1']}, 'then': 1, 'else': 0}},
                'loss': {'$cond': {'if': {'$eq': ['$result', '1-0']}, 'then': 1, 'else': 0}},
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
    side_percentages = {}
    for white in player_white_percentages:
        side_percentages['white'] = {'your wins': white['wins'], 'your losses': white['losses'],
                                     'your draws': white['draws']}
    for black in player_black_percentages:
        side_percentages['black'] = {'your wins': black['wins'], 'your losses': black['losses'],
                                     'your draws': black['draws']}
    names = Players.objects.filter(Q(name__ne=name) & Q(elo__gte=elo - r) & Q(elo__lte=elo + r)).distinct("name")
    other_players_white_percentages = Games.objects.aggregate([
        {
            '$match': {'white': {'$in': names}}
        },
        {
            '$project': {
                'win': {'$cond': {'if': {'$eq': ['$result', '1-0']}, 'then': 1, 'else': 0}},
                'loss': {'$cond': {'if': {'$eq': ['$result', '0-1']}, 'then': 1, 'else': 0}},
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
    other_players_black_percentages = Games.objects.aggregate([
        {
            '$match': {'black': {'$in': names}}
        },
        {
            '$project': {
                'win': {'$cond': {'if': {'$eq': ['$result', '0-1']}, 'then': 1, 'else': 0}},
                'loss': {'$cond': {'if': {'$eq': ['$result', '1-0']}, 'then': 1, 'else': 0}},
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
    for white in other_players_white_percentages:
        side_percentages['white']['other players wins'] = white['wins']
        side_percentages['white']['other players losses'] = white['losses']
        side_percentages['white']['other players draws'] = white['draws']
    for black in other_players_black_percentages:
        side_percentages['black']['other players wins'] = black['wins']
        side_percentages['black']['other players losses'] = black['losses']
        side_percentages['black']['other players draws'] = black['draws']
    response['general percentages'] = {'your wins': side_percentages['white']['your wins'] +
                                                    side_percentages['black']['your wins'],
                                       'other players wins': side_percentages['white']['other players wins'] +
                                                             side_percentages['black']['other players wins'],
                                       'your losses': side_percentages['white']['your losses'] +
                                                      side_percentages['black']['your losses'],
                                       'other players losses': side_percentages['white']['other players losses'] +
                                                               side_percentages['black']['other players losses'],
                                       'your draws': side_percentages['white']['your draws'] +
                                                     side_percentages['black']['your draws'],
                                       'other players draws': side_percentages['white']['other players draws'] +
                                                              side_percentages['black']['other players draws']}
    response['side percentages'] = {'white': side_percentages['white'], 'black': side_percentages['black']}
    return response


def calculate_event_comparisons(name, params):
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
    if "event" in params.keys():
        events = params["event"].split(",")
        player_event_stats = Games.objects.aggregate([
            {
                '$match': {'$and': [{'$or': [{'white': name}, {'black': name}]}, {'event': {'$in': events}}]}
            },
            {
                '$project': {
                    'event': 1,
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
                    '_id': '$event',
                    'wins': {'$sum': '$win'},
                    'losses': {'$sum': '$loss'},
                    'draws': {'$sum': '$draw'}
                }
            }
        ])
        player_event_stats_list = list(player_event_stats)
    else:
        player_event_stats = Games.objects.aggregate([
            {
                '$match': {'$or': [{'white': name}, {'black': name}]}
            },
            {
                '$project': {
                    'event': 1,
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
                    '_id': '$event',
                    'wins': {'$sum': '$win'},
                    'losses': {'$sum': '$loss'},
                    'draws': {'$sum': '$draw'}
                }
            }
        ])
        player_event_stats_list = list(player_event_stats)
        events = []
        for e in player_event_stats_list:
            events.append(e['_id'])
    names = Players.objects.filter(Q(name__ne=name) & Q(elo__gte=elo - r) & Q(elo__lte=elo + r)).distinct("name")
    event_stats = Games.objects.aggregate([
        {
            '$match': {'$and': [{'$or': [{'white': {'$in': names}}, {'black': {'$in': names}}]},
                                {'event': {'$in': events}}]}
        },
        {
            '$project': {
                'event': 1,
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
                '_id': '$event',
                'wins': {'$sum': '$win'},
                'losses': {'$sum': '$loss'},
                'draws': {'$sum': '$draw'}
            }
        }
    ])
    temp = list(event_stats)
    for player_event in player_event_stats_list:
        win_percentage = round((player_event['wins'] / (player_event['wins'] + player_event['losses'] +
                                                        player_event['draws'])) * 100, 2)
        loss_percentage = round((player_event['losses'] / (player_event['wins'] + player_event['losses'] +
                                                           player_event['draws'])) * 100, 2)
        draw_percentage = round((player_event['draws'] / (player_event['wins'] + player_event['losses'] +
                                                          player_event['draws'])) * 100, 2)
        for event in temp:
            if player_event['_id'] == event['_id']:
                other_win_percentage = round((event['wins'] / (event['wins'] + event['losses'] + event['draws']))
                                             * 100, 2)
                other_loss_percentage = round((event['losses'] / (event['wins'] + event['losses'] + event['draws']))
                                              * 100, 2)
                other_draw_percentage = round((event['draws'] / (event['wins'] + event['losses'] + event['draws']))
                                              * 100, 2)
                response[event['_id']] = {'your wins': player_event['wins'], 'other players wins': event['wins'],
                                          'your win percentage': win_percentage,
                                          'other players win percentage': other_win_percentage,
                                          'your losses': player_event['losses'],
                                          'other players losses': event['losses'],
                                          'your loss percentage': loss_percentage,
                                          'other players loss percentage': other_loss_percentage,
                                          'your draws': player_event['draws'], 'other players draws': event['draws'],
                                          'your draw percentage': draw_percentage,
                                          'other players draw percentage': other_draw_percentage}
        if player_event['_id'] not in response.keys():
            response[player_event['_id']] = {'your wins': player_event['wins'], 'other players wins': 0,
                                             'your win percentage': win_percentage, 'other players win percentage': 0,
                                             'your losses': player_event['losses'], 'other players losses': 0,
                                             'your loss percentage': loss_percentage,
                                             'other players loss percentage': 0,
                                             'your draws': player_event['draws'], 'other players draws': 0,
                                             'your draw percentage': draw_percentage,
                                             'other players draw percentage': 0}
    return response


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
