import re
from mongoengine import Q
from ChessDebriefer.Logic.games import evaluate_opening_database, evaluate_opening_engine
from ChessDebriefer.models import Openings


# TODO use database queries instead, add specific elo in the params (elo - r, elo + r) and specific eco
def calculate_eco_stats(eco, params):
    elo_pattern = re.compile(r'^\d{1,4}$')
    if params:
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
    else:
        min_elo = 0
        tournament = "false"
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
        dictionary = evaluate_opening_database(opening, min_elo, tournament)
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
