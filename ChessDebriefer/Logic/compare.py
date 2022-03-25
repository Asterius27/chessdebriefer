from mongoengine import Q
from ChessDebriefer.Logic.percentages_database import create_side_percentages_dictionary, create_percentages_dictionary
from ChessDebriefer.models import Games, Players

# TODO code cleanup


# TODO add percentages to response, (add params like date?)
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
    white_percentages = create_side_percentages_dictionary(name, {}, True)
    black_percentages = create_side_percentages_dictionary(name, {}, False)
    side_percentages = {'white': white_percentages['white'], 'black': black_percentages['black']}
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
        player_event_stats = create_percentages_dictionary(name, {}, 'event', events)
    else:
        player_event_stats = create_percentages_dictionary(name, {}, 'event', [])
        events = []
        for key in player_event_stats.keys():
            events.append(key)
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
    for key in player_event_stats:
        for event in temp:
            if key == event['_id']:
                other_win_percentage = round((event['wins'] / (event['wins'] + event['losses'] + event['draws']))
                                             * 100, 2)
                other_loss_percentage = round((event['losses'] / (event['wins'] + event['losses'] + event['draws']))
                                              * 100, 2)
                other_draw_percentage = round((event['draws'] / (event['wins'] + event['losses'] + event['draws']))
                                              * 100, 2)
                response[event['_id']] = player_event_stats[key]
                # TODO
                response[event['_id']] = {'other players wins': event['wins'],
                                          'other players win percentage': other_win_percentage,
                                          'other players losses': event['losses'],
                                          'other players loss percentage': other_loss_percentage,
                                          'other players draws': event['draws'],
                                          'other players draw percentage': other_draw_percentage}
        if key not in response.keys():
            response[key] = player_event_stats[key]
            # TODO
            response[key] = {'other players wins': 0, 'other players win percentage': 0, 'other players losses': 0,
                             'other players loss percentage': 0, 'other players draws': 0,
                             'other players draw percentage': 0}
    return response


def calculate_termination_comparisons(name, params):
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
    if "termination" in params.keys():
        terminations = params["termination"].split(",")
        player_termination_stats = create_percentages_dictionary(name, {}, 'termination', terminations)
    else:
        player_termination_stats = create_percentages_dictionary(name, {}, 'termination', [])
        terminations = []
        for key in player_termination_stats.keys():
            terminations.append(key)
    names = Players.objects.filter(Q(name__ne=name) & Q(elo__gte=elo - r) & Q(elo__lte=elo + r)).distinct("name")
    termination_stats = Games.objects.aggregate([
        {
            '$match': {'$and': [{'$or': [{'white': {'$in': names}}, {'black': {'$in': names}}]},
                                {'termination': {'$in': terminations}}]}
        },
        {
            '$project': {
                'termination': 1,
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
                '_id': '$termination',
                'wins': {'$sum': '$win'},
                'losses': {'$sum': '$loss'},
                'draws': {'$sum': '$draw'}
            }
        }
    ])  # TODO not too fast don't know if it's fixable
    temp = list(termination_stats)
    for key in player_termination_stats:
        for termination in temp:
            if key == termination['_id']:
                other_win_percentage = round((termination['wins'] / (termination['wins'] + termination['losses'] +
                                                                     termination['draws'])) * 100, 2)
                other_loss_percentage = round((termination['losses'] / (termination['wins'] + termination['losses'] +
                                                                        termination['draws'])) * 100, 2)
                other_draw_percentage = round((termination['draws'] / (termination['wins'] + termination['losses'] +
                                                                       termination['draws'])) * 100, 2)
                response[termination['_id']] = player_termination_stats[key]
                response[termination['_id']] = {'other players wins': termination['wins'],
                                                'other players win percentage': other_win_percentage,
                                                'other players losses': termination['losses'],
                                                'other players loss percentage': other_loss_percentage,
                                                'other players draws': termination['draws'],
                                                'other players draw percentage': other_draw_percentage}
        if key not in response.keys():
            response[key] = player_termination_stats[key]
            response[key] = {'other players wins': 0, 'other players win percentage': 0, 'other players losses': 0,
                             'other players loss percentage': 0, 'other players draws': 0,
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
        player_eco_stats = create_percentages_dictionary(name, {}, 'eco', ecos)
    else:
        player_eco_stats = create_percentages_dictionary(name, {}, 'eco', [])
        ecos = []
        for key in player_eco_stats:
            ecos.append(key)
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
    for key in player_eco_stats:
        for eco in temp:
            if key == eco['_id']:
                other_win_percentage = round((eco['wins'] / (eco['wins'] + eco['losses'] + eco['draws'])) * 100, 2)
                other_loss_percentage = round((eco['losses'] / (eco['wins'] + eco['losses'] + eco['draws'])) * 100, 2)
                other_draw_percentage = round((eco['draws'] / (eco['wins'] + eco['losses'] + eco['draws'])) * 100, 2)
                response[eco['_id']] = player_eco_stats[key]
                response[eco['_id']] = {'other players wins': eco['wins'],
                                        'other players win percentage': other_win_percentage,
                                        'other players losses': eco['losses'],
                                        'other players loss percentage': other_loss_percentage,
                                        'other players draws': eco['draws'],
                                        'other players draw percentage': other_draw_percentage}
        if key not in response.keys():
            response[key] = player_eco_stats[key]
            response[key] = {'other players wins': 0, 'other players win percentage': 0, 'other players losses': 0,
                             'other players loss percentage': 0, 'other players draws': 0,
                             'other players draw percentage': 0}
    return response


def create_other_players_percentages_dictionary():
    dictionary = {}
    return dictionary
