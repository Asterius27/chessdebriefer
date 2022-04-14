from mongoengine import Q
import chess.syzygy
from ChessDebriefer.Logic.compare import check_params_comparisons
from ChessDebriefer.Logic.endgames import calculate_endgame_percentages, calculate_endgame_material_percentages, \
    calculate_endgame_wdl_material_percentages, create_material_dictionary, \
    calculate_endgame_predicted_wdl_material_percentages, calculate_endgame_tablebase_percentages, \
    calculate_endgame_predicted_wdl_tablebase_percentages, material_advantage, tablebase_evaluation
from ChessDebriefer.Logic.percentages import calculate_wdl_percentages
from ChessDebriefer.models import Games


def calculate_compare_endgame_percentages(name, params):
    elo, r = check_params_comparisons(name, params)
    temp = {'minelo': str(elo - r), 'maxelo': str(elo + r), 'pieces': '5'}
    response = calculate_endgame_percentages(name, temp)
    games = compare_database_query(name, temp)
    i, white_wins, white_losses, white_draws, black_wins, black_losses, black_draws = calculate_general_wdl_compare(
        name, games, elo, r)
    percentage_won, percentage_lost, percentage_drawn = calculate_wdl_percentages(white_wins + black_wins,
                                                                                  white_losses + black_losses,
                                                                                  white_draws + black_draws)
    percentage_won_w, percentage_lost_w, percentage_drawn_w = calculate_wdl_percentages(white_wins, white_losses,
                                                                                        white_draws)
    percentage_won_b, percentage_lost_b, percentage_drawn_b = calculate_wdl_percentages(black_wins, black_losses,
                                                                                        black_draws)
    response['general percentages'].update({'other players games': i, 'other players wins': white_wins + black_wins,
                                            'other players losses': white_losses + black_losses,
                                            'other players draws': white_draws + black_draws,
                                            'other players win percentage': percentage_won,
                                            'other players loss percentage': percentage_lost,
                                            'other players draw percentage': percentage_drawn})
    response['side percentages']['white'].update({'other players wins': white_wins,
                                                  'other players losses': white_losses,
                                                  'other players draws': white_draws,
                                                  'other players win percentage': percentage_won_w,
                                                  'other players loss percentage': percentage_lost_w,
                                                  'other players draw percentage': percentage_drawn_w})
    response['side percentages']['black'].update({'other players wins': black_wins,
                                                  'other players losses': black_losses,
                                                  'other players draws': black_draws,
                                                  'other players win percentage': percentage_won_b,
                                                  'other players loss percentage': percentage_lost_b,
                                                  'other players draw percentage': percentage_drawn_b})
    return response


def calculate_compare_endgame_material(name, params):
    elo, r = check_params_comparisons(name, params)
    temp = {'minelo': str(elo - r), 'maxelo': str(elo + r), 'pieces': '5'}
    response = calculate_endgame_material_percentages(name, temp)
    games = compare_database_query(name, temp)
    wins, losses, draws, win_material_adv, loss_material_adv, draw_material_adv = calculate_wdl_material_compare(
        name, games, 5, elo, r)
    response.update({'other players wins': wins,
                     'matches other players should have won (material advantage)': win_material_adv,
                     'other players losses': losses,
                     'matches other players should have lost (material disadvantage)': losses - loss_material_adv,
                     'other players draws': draws, 'other players draws with material advantage': draw_material_adv,
                     'other players draws with material disadvantage': draws - draw_material_adv})
    return response


def calculate_compare_endgame_wdl_material(name, params):
    response = {}
    elo, r = check_params_comparisons(name, params)
    temp = {'minelo': str(elo - r), 'maxelo': str(elo + r), 'pieces': '5'}
    response["your stats"] = calculate_endgame_wdl_material_percentages(name, temp)
    games = compare_database_query(name, temp)
    wins, losses, draws, win_material_adv, loss_material_adv, draw_material_adv = calculate_wdl_material_compare(
        name, games, 5, elo, r)
    dictionary = create_material_dictionary(wins, losses, draws, win_material_adv, loss_material_adv, draw_material_adv)
    response["other players stats"] = dictionary
    return response


def calculate_compare_endgame_predicted_wdl_material(name, params):
    elo, r = check_params_comparisons(name, params)
    temp = {'minelo': str(elo - r), 'maxelo': str(elo + r), 'pieces': '5'}
    response = calculate_endgame_predicted_wdl_material_percentages(name, temp)
    games = compare_database_query(name, temp)
    white_wins, white_losses, white_draws, black_wins, black_losses, black_draws = \
        calculate_predicted_wdl_material_compare(name, games, 5, elo, r)
    percentage_won, percentage_lost, percentage_drawn = calculate_wdl_percentages(white_wins + black_wins,
                                                                                  white_losses + black_losses,
                                                                                  white_draws + black_draws)
    percentage_won_w, percentage_lost_w, percentage_drawn_w = calculate_wdl_percentages(white_wins, white_losses,
                                                                                        white_draws)
    percentage_won_b, percentage_lost_b, percentage_drawn_b = calculate_wdl_percentages(black_wins, black_losses,
                                                                                        black_draws)
    response['general percentages'].update({'other players wins': white_wins + black_wins,
                                            'other players losses': white_losses + black_losses,
                                            'other players draws': white_draws + black_draws,
                                            'other players win percentage': percentage_won,
                                            'other players loss percentage': percentage_lost,
                                            'other players draw percentage': percentage_drawn})
    response['side percentages']['white'].update({'other players wins': white_wins,
                                                  'other players losses': white_losses,
                                                  'other players draws': white_draws,
                                                  'other players win percentage': percentage_won_w,
                                                  'other players loss percentage': percentage_lost_w,
                                                  'other players draw percentage': percentage_drawn_w})
    response['side percentages']['black'].update({'other players wins': black_wins,
                                                  'other players losses': black_losses,
                                                  'other players draws': black_draws,
                                                  'other players win percentage': percentage_won_b,
                                                  'other players loss percentage': percentage_lost_b,
                                                  'other players draw percentage': percentage_drawn_b})
    return response


# TODO slow only first time? problem is method struct.unpack_from that is used by the python chess library. It's slow
#  but it uses a cache so only first time (for each player) is slow. Cache is reset after pc restart, how big is it?
#  Is it possible to fill it completely? What happens performance-wise when it is filled?
def calculate_compare_endgame_tablebase(name, params):
    elo, r = check_params_comparisons(name, params)
    temp = {'minelo': str(elo - r), 'maxelo': str(elo + r)}
    response = calculate_endgame_tablebase_percentages(name, temp)
    games = compare_database_query(name, temp)
    wins, losses, draws, win_predict, loss_predict, draw_predict = calculate_wdl_tablebase_compare(
        name, games, 5, elo, r)
    response.update({'other players wins': wins, 'matches other players should have won': win_predict,
                     'other players losses': losses, 'matches other players should have lost': loss_predict,
                     'other players draws': draws, 'matches other players should have drawn': draw_predict})
    return response


def calculate_compare_endgame_predicted_wdl_tablebase(name, params):
    elo, r = check_params_comparisons(name, params)
    temp = {'minelo': str(elo - r), 'maxelo': str(elo + r), 'pieces': '5'}
    response = calculate_endgame_predicted_wdl_tablebase_percentages(name, temp)
    games = compare_database_query(name, temp)
    white_wins, white_losses, white_draws, black_wins, black_losses, black_draws = \
        calculate_predicted_wdl_tablebase_compare(name, games, 5, elo, r)
    percentage_won, percentage_lost, percentage_drawn = calculate_wdl_percentages(white_wins + black_wins,
                                                                                  white_losses + black_losses,
                                                                                  white_draws + black_draws)
    percentage_won_w, percentage_lost_w, percentage_drawn_w = calculate_wdl_percentages(white_wins, white_losses,
                                                                                        white_draws)
    percentage_won_b, percentage_lost_b, percentage_drawn_b = calculate_wdl_percentages(black_wins, black_losses,
                                                                                        black_draws)
    response['general percentages'].update({'other players wins': white_wins + black_wins,
                                            'other players losses': white_losses + black_losses,
                                            'other players draws': white_draws + black_draws,
                                            'other players win percentage': percentage_won,
                                            'other players loss percentage': percentage_lost,
                                            'other players draw percentage': percentage_drawn})
    response['side percentages']['white'].update({'other players wins': white_wins,
                                                  'other players losses': white_losses,
                                                  'other players draws': white_draws,
                                                  'other players win percentage': percentage_won_w,
                                                  'other players loss percentage': percentage_lost_w,
                                                  'other players draw percentage': percentage_drawn_w})
    response['side percentages']['black'].update({'other players wins': black_wins,
                                                  'other players losses': black_losses,
                                                  'other players draws': black_draws,
                                                  'other players win percentage': percentage_won_b,
                                                  'other players loss percentage': percentage_lost_b,
                                                  'other players draw percentage': percentage_drawn_b})
    return response


def compare_database_query(name, params):
    min_elo = int(params["minelo"])
    max_elo = int(params["maxelo"])
    games = Games.objects.filter(((Q(white__ne=name) & Q(white_elo__gte=min_elo) & Q(white_elo__lte=max_elo)) |
                                 (Q(black__ne=name) & Q(black_elo__gte=min_elo) & Q(black_elo__lte=max_elo))) &
                                 Q(five_piece_endgame_fen__ne=""))
    return games


def calculate_general_wdl_compare(name, games, elo, r):
    i = 0
    white_wins = 0
    white_losses = 0
    black_wins = 0
    black_losses = 0
    white_draws = 0
    black_draws = 0
    for game in games:
        i += 1
        if game.result == '1-0':
            if game.white != name and (elo - r) <= game.white_elo <= (elo + r):
                white_wins += 1
            if game.black != name and (elo - r) <= game.black_elo <= (elo + r):
                black_losses += 1
        if game.result == '0-1':
            if game.white != name and (elo - r) <= game.white_elo <= (elo + r):
                white_losses += 1
            if game.black != name and (elo - r) <= game.black_elo <= (elo + r):
                black_wins += 1
        if game.result == '1/2-1/2':
            if game.white != name and (elo - r) <= game.white_elo <= (elo + r):
                white_draws += 1
            if game.black != name and (elo - r) <= game.black_elo <= (elo + r):
                black_draws += 1
    return i, white_wins, white_losses, white_draws, black_wins, black_losses, black_draws


def calculate_predicted_wdl_material_compare(name, games, pieces, elo, r):
    white_wins = 0
    white_losses = 0
    white_draws = 0
    black_wins = 0
    black_losses = 0
    black_draws = 0
    for game in games:
        if game.white != name and (elo - r) <= game.white_elo <= (elo + r):
            adv = material_advantage(pieces, game.five_piece_endgame_fen, True)
            if adv == 1:
                white_wins += 1
            elif adv == -1:
                white_losses += 1
            elif adv == 0:
                white_draws += 1
        if game.black != name and (elo - r) <= game.black_elo <= (elo + r):
            adv = material_advantage(pieces, game.five_piece_endgame_fen, False)
            if adv == 1:
                black_wins += 1
            elif adv == -1:
                black_losses += 1
            elif adv == 0:
                black_draws += 1
    return white_wins, white_losses, white_draws, black_wins, black_losses, black_draws


def calculate_wdl_material_compare(name, games, pieces, elo, r):
    wins = 0
    losses = 0
    draws = 0
    win_material_adv = 0
    loss_material_adv = 0
    draw_material_adv = 0
    for game in games:
        if game.white != name and (elo - r) <= game.white_elo <= (elo + r):
            adv = material_advantage(pieces, game.five_piece_endgame_fen, True)
            if game.result == "1-0":
                wins += 1
                if adv == 1:
                    win_material_adv += 1
            if game.result == "0-1":
                losses += 1
                if adv == 1:
                    loss_material_adv += 1
            if game.result == "1/2-1/2":
                draws += 1
                if adv == 1:
                    draw_material_adv += 1
        if game.black != name and (elo - r) <= game.black_elo <= (elo + r):
            adv = material_advantage(pieces, game.five_piece_endgame_fen, False)
            if game.result == "1-0":
                losses += 1
                if adv == 1:
                    loss_material_adv += 1
            if game.result == "0-1":
                wins += 1
                if adv == 1:
                    win_material_adv += 1
            if game.result == "1/2-1/2":
                draws += 1
                if adv == 1:
                    draw_material_adv += 1
    return wins, losses, draws, win_material_adv, loss_material_adv, draw_material_adv


def calculate_predicted_wdl_tablebase_compare(name, games, pieces, elo, r):
    white_wins = 0
    white_losses = 0
    white_draws = 0
    black_wins = 0
    black_losses = 0
    black_draws = 0
    with chess.syzygy.open_tablebase("syzygy345pieces") as tb:
        for game in games:
            if game.white != name and (elo - r) <= game.white_elo <= (elo + r):
                adv = tablebase_evaluation(tb, game.five_piece_endgame_fen, pieces, True)
                if adv == 1:
                    white_wins += 1
                elif adv == -1:
                    white_losses += 1
                elif adv == 0:
                    white_draws += 1
            if game.black != name and (elo - r) <= game.black_elo <= (elo + r):
                adv = tablebase_evaluation(tb, game.five_piece_endgame_fen, pieces, False)
                if adv == 1:
                    black_wins += 1
                elif adv == -1:
                    black_losses += 1
                elif adv == 0:
                    black_draws += 1
    return white_wins, white_losses, white_draws, black_wins, black_losses, black_draws


def calculate_wdl_tablebase_compare(name, games, pieces, elo, r):
    wins = 0
    losses = 0
    draws = 0
    win_predict = 0
    loss_predict = 0
    draw_predict = 0
    with chess.syzygy.open_tablebase("syzygy345pieces") as tb:
        for game in games:
            if game.white != name and (elo - r) <= game.white_elo <= (elo + r):
                adv = tablebase_evaluation(tb, game.five_piece_endgame_fen, pieces, True)
                if adv != 2:
                    if game.result == "1-0":
                        wins += 1
                        if adv == 1:
                            win_predict += 1
                    if game.result == "0-1":
                        losses += 1
                        if adv == -1:
                            loss_predict += 1
                    if game.result == "1/2-1/2":
                        draws += 1
                        if adv == 0:
                            draw_predict += 1
            if game.black != name and (elo - r) <= game.black_elo <= (elo + r):
                adv = tablebase_evaluation(tb, game.five_piece_endgame_fen, pieces, False)
                if adv != 2:
                    if game.result == "1-0":
                        losses += 1
                        if adv == -1:
                            loss_predict += 1
                    if game.result == "0-1":
                        wins += 1
                        if adv == 1:
                            win_predict += 1
                    if game.result == "1/2-1/2":
                        draws += 1
                        if adv == 0:
                            draw_predict += 1
    return wins, losses, draws, win_predict, loss_predict, draw_predict
