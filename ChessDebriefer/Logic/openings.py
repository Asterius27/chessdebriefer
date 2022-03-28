import re
from mongoengine import Q
from ChessDebriefer.Logic.games import evaluate_opening_engine
from ChessDebriefer.models import Openings, Games


def calculate_eco_stats(eco, params):
    elo_pattern = re.compile(r'^\d{1,4}$')
    if "min_elo" in params.keys():
        if elo_pattern.match(params["min_elo"]):
            min_elo = int(params["min_elo"])
        else:
            min_elo = 0
    else:
        min_elo = 0
    if "tournament" in params.keys():
        if params["tournament"] == "false" or params["tournament"] == "true":
            tournament = params["tournament"]
        else:
            tournament = "false"
    else:
        tournament = "false"
    if min_elo == 0:
        if "elo" in params.keys():
            if "range" in params.keys():
                r = params["range"]
            else:
                r = 100
            min_elo = params.keys["elo"] - r
            max_elo = params.keys["elo"] + r
        else:
            max_elo = 9999
    else:
        max_elo = 9999
    openings = Openings.objects.filter(Q(eco=eco))
    response = {}
    variations = {}
    eco_white_wins = 0
    eco_black_wins = 0
    eco_draws = 0
    percentage_eco_white_wins = 0.
    percentage_eco_black_wins = 0.
    percentage_eco_draws = 0.
    i = 0
    for opening in openings:
        if opening.black_opening != "?":
            name = opening.white_opening + " " + opening.black_opening
        else:
            name = opening.white_opening
        dictionary = calculate_variation_stats(opening.id, min_elo, max_elo, tournament)
        evaluate_opening_engine(opening)
        dictionary["engine_evaluation"] = float(opening.engine_evaluation)
        if name not in variations.keys():
            variations[name] = dictionary
        else:
            variations[name + " " + str(i)] = dictionary
            i = i + 1
        eco_white_wins = eco_white_wins + dictionary["white_wins"]
        eco_black_wins = eco_black_wins + dictionary["black_wins"]
        eco_draws = eco_draws + dictionary["draws"]
    if eco_white_wins + eco_black_wins + eco_draws != 0:
        percentage_eco_white_wins = round((eco_white_wins / (eco_white_wins + eco_black_wins + eco_draws)) * 100, 2)
        percentage_eco_black_wins = round((eco_black_wins / (eco_white_wins + eco_black_wins + eco_draws)) * 100, 2)
        percentage_eco_draws = round((eco_draws / (eco_white_wins + eco_black_wins + eco_draws)) * 100, 2)
    response[eco] = {"white_wins": eco_white_wins, "black_wins": eco_black_wins, "draws": eco_draws,
                     "percentage_white_wins": percentage_eco_white_wins,
                     "percentage_black_wins": percentage_eco_black_wins, "percentage_draws_wins": percentage_eco_draws}
    response["variations"] = variations
    return response


def calculate_variation_stats(opening, min_elo, max_elo, tournament):
    dictionary = {'white_wins': 0, 'black_wins': 0, 'draws': 0, 'white_win_percentage': 0., 'black_win_percentage': 0.,
                  'draw_percentage': 0.}
    if tournament == "true":
        match_query = {
            '$match': {'$and': [{'opening_id': opening}, {'white_elo': {'$gt': min_elo, '$lt': max_elo}},
                                {'black_elo': {'$gt': min_elo, '$lt': max_elo}}, {'event': {'$regex': 'tournament'}}]}
        }
    else:
        match_query = {
            '$match': {'$and': [{'opening_id': opening}, {'white_elo': {'$gt': min_elo, '$lt': max_elo}},
                                {'black_elo': {'$gt': min_elo, '$lt': max_elo}}]}
        }
    opening_stats = Games.objects.aggregate([
        match_query,
        {
            '$project': {
                'white_win': {'$cond': {'if': {'$eq': ['$result', '1-0']}, 'then': 1, 'else': 0}},
                'black_win': {'$cond': {'if': {'$eq': ['$result', '0-1']}, 'then': 1, 'else': 0}},
                'draw': {'$cond': {'if': {'$eq': ['$result', '1/2-1/2']}, 'then': 1, 'else': 0}},
            }
        },
        {
            '$group': {
                '_id': 'null',
                'white_wins': {'$sum': '$white_win'},
                'black_wins': {'$sum': '$black_win'},
                'draws': {'$sum': '$draw'}
            }
        },
        {
            '$project': {
                '_id': 0,
                'white_wins': 1,
                'black_wins': 1,
                'draws': 1,
                'white_win_percentage': {'$round': [
                    {'$multiply': [{'$divide': [
                        '$white_wins', {'$add': ['$white_wins', '$black_wins', '$draws']}
                    ]}, 100]}, 2
                ]},
                'black_win_percentage': {'$round': [
                    {'$multiply': [{'$divide': [
                        '$black_wins', {'$add': ['$white_wins', '$black_wins', '$draws']}
                    ]}, 100]}, 2
                ]},
                'draw_percentage': {'$round': [
                    {'$multiply': [{'$divide': [
                        '$draws', {'$add': ['$white_wins', '$black_wins', '$draws']}
                    ]}, 100]}, 2
                ]}
            }
        }
    ])
    for op in opening_stats:
        dictionary = op
    return dictionary
