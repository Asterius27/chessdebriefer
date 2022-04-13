import io
import chess.pgn
import chess.syzygy
from chess import Board
from mongoengine import Q
from ChessDebriefer.Logic.compare import check_params_comparisons
from ChessDebriefer.Logic.percentages import check_params, calculate_wdl_percentages
from ChessDebriefer.models import Games

# TODO remove duplicate code (?)


def calculate_endgame_percentages(name, params):
    response = {}
    white_wins = 0
    white_losses = 0
    black_wins = 0
    black_losses = 0
    white_draws = 0
    black_draws = 0
    n_endgame_games, n_games, endgame_games, pieces = database_query(name, params)
    percentage_endgames = round((n_endgame_games / (n_games * 1.)) * 100, 2)
    for (game, parsed_game) in endgame_games:
        if game.result == '1-0':
            if game.white == name:
                white_wins += 1
            if game.black == name:
                black_losses += 1
        if game.result == '0-1':
            if game.white == name:
                white_losses += 1
            if game.black == name:
                black_wins += 1
        if game.result == '1/2-1/2':
            if game.white == name:
                white_draws += 1
            if game.black == name:
                black_draws += 1
    percentage_won, percentage_lost, percentage_drawn = calculate_wdl_percentages(white_wins + black_wins,
                                                        white_losses + black_losses, white_draws + black_draws)
    percentage_won_w, percentage_lost_w, percentage_drawn_w = calculate_wdl_percentages(white_wins, white_losses,
                                                                                        white_draws)
    percentage_won_b, percentage_lost_b, percentage_drawn_b = calculate_wdl_percentages(black_wins, black_losses,
                                                                                        black_draws)
    response['general percentages'] = {'games': n_games, 'endgames': n_endgame_games,
                                       'percentage of games that finish in the endgame': percentage_endgames,
                                       'wins': white_wins + black_wins, 'losses': white_losses + black_losses,
                                       'draws': white_draws + black_draws, 'win percentage': percentage_won,
                                       'loss percentage': percentage_lost, 'draw percentage': percentage_drawn}
    response['side percentages'] = {}
    response['side percentages']['white'] = {'wins': white_wins, 'losses': white_losses, 'draws': white_draws,
                                             'win percentage': percentage_won_w, 'loss percentage': percentage_lost_w,
                                             'draw percentage': percentage_drawn_w}
    response['side percentages']['black'] = {'wins': black_wins, 'losses': black_losses, 'draws': black_draws,
                                             'win percentage': percentage_won_b, 'loss percentage': percentage_lost_b,
                                             'draw percentage': percentage_drawn_b}
    return response


def calculate_endgame_material_percentages(name, params):
    wins = 0
    losses = 0
    draws = 0
    win_material_adv = 0
    loss_material_adv = 0
    draw_material_adv = 0
    n_endgame_games, n_games, endgame_games, pieces = database_query(name, params)
    for (game, parsed_game) in endgame_games:
        if game.white == name:
            adv = material_advantage(pieces, parsed_game, True)
            if game.result == "1-0":
                wins += 1
                if adv:
                    win_material_adv += 1
            if game.result == "0-1":
                losses += 1
                if adv:
                    loss_material_adv += 1
            if game.result == "1/2-1/2":
                draws += 1
                if adv:
                    draw_material_adv += 1
        else:
            adv = material_advantage(pieces, parsed_game, False)
            if game.result == "1-0":
                losses += 1
                if adv:
                    loss_material_adv += 1
            if game.result == "0-1":
                wins += 1
                if adv:
                    win_material_adv += 1
            if game.result == "1/2-1/2":
                draws += 1
                if adv:
                    draw_material_adv += 1
    return {'wins': wins, 'matches you should have won (material advantage)': win_material_adv, 'losses': losses,
            'matches you should have lost (material disadvantage)': losses - loss_material_adv, 'draws': draws,
            'draws with material advantage': draw_material_adv,
            'draws with material disadvantage': draws - draw_material_adv}


def calculate_endgame_wdl_material_percentages(name, params):
    response = {}
    wins = 0
    losses = 0
    draws = 0
    win_material_adv = 0
    loss_material_adv = 0
    draw_material_adv = 0
    n_endgame_games, n_games, endgame_games, pieces = database_query(name, params)
    for (game, parsed_game) in endgame_games:
        if game.white == name:
            adv = material_advantage(pieces, parsed_game, True)
            if game.result == "1-0":
                wins += 1
                if adv:
                    win_material_adv += 1
            if game.result == "0-1":
                losses += 1
                if adv:
                    loss_material_adv += 1
            if game.result == "1/2-1/2":
                draws += 1
                if adv:
                    draw_material_adv += 1
        else:
            adv = material_advantage(pieces, parsed_game, False)
            if game.result == "1-0":
                losses += 1
                if adv:
                    loss_material_adv += 1
            if game.result == "0-1":
                wins += 1
                if adv:
                    win_material_adv += 1
            if game.result == "1/2-1/2":
                draws += 1
                if adv:
                    draw_material_adv += 1
    response["material advantage"] = {'wins': win_material_adv, 'losses': loss_material_adv, 'draws': draw_material_adv}
    response["material disadvantage"] = {'wins': wins - win_material_adv, 'losses': losses - loss_material_adv,
                                         'draws': draws - draw_material_adv}
    percentage_won_a, percentage_lost_a, percentage_drawn_a = calculate_wdl_percentages(win_material_adv,
                                                                                        loss_material_adv,
                                                                                        draw_material_adv)
    percentage_won_d, percentage_lost_d, percentage_drawn_d = calculate_wdl_percentages(wins - win_material_adv,
                                                                                        losses - loss_material_adv,
                                                                                        draws - draw_material_adv)
    response["material advantage"].update({'percentage won': percentage_won_a, 'percentage lost': percentage_lost_a,
                                           'percentage drawn': percentage_drawn_a})
    response["material disadvantage"].update({'percentage won': percentage_won_d, 'percentage lost': percentage_lost_d,
                                              'percentage drawn': percentage_drawn_d})
    return response


def calculate_endgame_tablebase_percentages(name, params):
    wins = 0
    losses = 0
    draws = 0
    win_predict = 0
    loss_predict = 0
    draw_predict = 0
    params_copy = params.copy()
    params_copy["pieces"] = "5"
    n_endgame_games, n_games, endgame_games, pieces = database_query(name, params_copy)
    with chess.syzygy.open_tablebase("syzygy345pieces") as tb:
        for (game, parsed_game) in endgame_games:
            if game.white == name:
                adv = tablebase_evaluation(tb, parsed_game, pieces, True)
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
            else:
                adv = tablebase_evaluation(tb, parsed_game, pieces, False)
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
    return {'wins': wins, 'matches you should have won': win_predict, 'losses': losses,
            'matches you should have lost': loss_predict, 'draws': draws, 'matches you should have drawn': draw_predict}


def calculate_compare_endgame_percentages(name, params):
    i = 0
    white_wins = 0
    white_losses = 0
    black_wins = 0
    black_losses = 0
    white_draws = 0
    black_draws = 0
    elo, r = check_params_comparisons(name, params)
    temp = {'minelo': str(elo - r), 'maxelo': str(elo + r), 'pieces': '5'}
    response = calculate_endgame_percentages(name, temp)
    games = compare_database_query(name, temp)
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
    wins = 0
    losses = 0
    draws = 0
    win_material_adv = 0
    loss_material_adv = 0
    draw_material_adv = 0
    elo, r = check_params_comparisons(name, params)
    temp = {'minelo': str(elo - r), 'maxelo': str(elo + r), 'pieces': '5'}
    response = calculate_endgame_material_percentages(name, temp)
    games = compare_database_query(name, temp)
    for game in games:
        if game.white != name and (elo - r) <= game.white_elo <= (elo + r):
            adv = material_advantage(5, game.five_piece_endgame_fen, True)
            if game.result == "1-0":
                wins += 1
                if adv:
                    win_material_adv += 1
            if game.result == "0-1":
                losses += 1
                if adv:
                    loss_material_adv += 1
            if game.result == "1/2-1/2":
                draws += 1
                if adv:
                    draw_material_adv += 1
        if game.black != name and (elo - r) <= game.black_elo <= (elo + r):
            adv = material_advantage(5, game.five_piece_endgame_fen, False)
            if game.result == "1-0":
                losses += 1
                if adv:
                    loss_material_adv += 1
            if game.result == "0-1":
                wins += 1
                if adv:
                    win_material_adv += 1
            if game.result == "1/2-1/2":
                draws += 1
                if adv:
                    draw_material_adv += 1
    response.update({'other players wins': wins,
                     'matches other players should have won (material advantage)': win_material_adv,
                     'other players losses': losses,
                     'matches other players should have lost (material disadvantage)': losses - loss_material_adv,
                     'other players draws': draws, 'other players draws with material advantage': draw_material_adv,
                     'other players draws with material disadvantage': draws - draw_material_adv})
    return response


def calculate_compare_endgame_wdl_material(name, params):
    response = {}
    wins = 0
    losses = 0
    draws = 0
    win_material_adv = 0
    loss_material_adv = 0
    draw_material_adv = 0
    elo, r = check_params_comparisons(name, params)
    temp = {'minelo': str(elo - r), 'maxelo': str(elo + r), 'pieces': '5'}
    response["your stats"] = calculate_endgame_wdl_material_percentages(name, temp)
    games = compare_database_query(name, temp)
    for game in games:
        if game.white != name and (elo - r) <= game.white_elo <= (elo + r):
            adv = material_advantage(5, game.five_piece_endgame_fen, True)
            if game.result == "1-0":
                wins += 1
                if adv:
                    win_material_adv += 1
            if game.result == "0-1":
                losses += 1
                if adv:
                    loss_material_adv += 1
            if game.result == "1/2-1/2":
                draws += 1
                if adv:
                    draw_material_adv += 1
        if game.black != name and (elo - r) <= game.black_elo <= (elo + r):
            adv = material_advantage(5, game.five_piece_endgame_fen, False)
            if game.result == "1-0":
                losses += 1
                if adv:
                    loss_material_adv += 1
            if game.result == "0-1":
                wins += 1
                if adv:
                    win_material_adv += 1
            if game.result == "1/2-1/2":
                draws += 1
                if adv:
                    draw_material_adv += 1
    dictionary = {}
    dictionary["material advantage"] = {'wins': win_material_adv, 'losses': loss_material_adv,
                                        'draws': draw_material_adv}
    dictionary["material disadvantage"] = {'wins': wins - win_material_adv, 'losses': losses - loss_material_adv,
                                           'draws': draws - draw_material_adv}
    percentage_won_a, percentage_lost_a, percentage_drawn_a = calculate_wdl_percentages(win_material_adv,
                                                                                        loss_material_adv,
                                                                                        draw_material_adv)
    percentage_won_d, percentage_lost_d, percentage_drawn_d = calculate_wdl_percentages(wins - win_material_adv,
                                                                                        losses - loss_material_adv,
                                                                                        draws - draw_material_adv)
    dictionary["material advantage"].update({'percentage won': percentage_won_a, 'percentage lost': percentage_lost_a,
                                             'percentage drawn': percentage_drawn_a})
    dictionary["material disadvantage"].update({'percentage won': percentage_won_d,
                                                'percentage lost': percentage_lost_d,
                                                'percentage drawn': percentage_drawn_d})
    response["other players stats"] = dictionary
    return response


# TODO slow only first time? problem is method struct.unpack_from but it's hard to replicate
#  (seems to happen only on first invocation for each player after pc restart)
#  struct class uses a cache that's why probably
def calculate_compare_endgame_tablebase(name, params):
    wins = 0
    losses = 0
    draws = 0
    win_predict = 0
    loss_predict = 0
    draw_predict = 0
    elo, r = check_params_comparisons(name, params)
    temp = {'minelo': str(elo - r), 'maxelo': str(elo + r)}
    response = calculate_endgame_tablebase_percentages(name, temp)
    games = compare_database_query(name, temp)
    with chess.syzygy.open_tablebase("syzygy345pieces") as tb:
        for game in games:
            if game.white != name and (elo - r) <= game.white_elo <= (elo + r):
                adv = tablebase_evaluation(tb, game.five_piece_endgame_fen, 5, True)
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
                adv = tablebase_evaluation(tb, game.five_piece_endgame_fen, 5, False)
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
    response.update({'other players wins': wins, 'matches other players should have won': win_predict,
                     'other players losses': losses, 'matches other players should have lost': loss_predict,
                     'other players draws': draws, 'matches other players should have drawn': draw_predict})
    return response


def database_query(name, params):
    pieces, from_date, to_date, min_elo, max_elo, opponent = check_endgame_params(params)
    if opponent:
        games = Games.objects.filter(((Q(white=name) & Q(black=opponent) & Q(white_elo__gte=min_elo) &
                                       Q(white_elo__lte=max_elo)) | (Q(black=name) & Q(white=opponent) &
                                                                     Q(black_elo__gte=min_elo) &
                                                                     Q(black_elo__lte=max_elo)))
                                     & Q(date__gte=from_date) & Q(date__lte=to_date))
    else:
        games = Games.objects.filter(((Q(white=name) & Q(white_elo__gte=min_elo) & Q(white_elo__lte=max_elo)) |
                                      (Q(black=name) & Q(black_elo__gte=min_elo) & Q(black_elo__lte=max_elo)))
                                     & Q(date__gte=from_date) & Q(date__lte=to_date))
    n_endgame_games, n_games, endgame_games = find_endgame_matches(pieces, games)
    return n_endgame_games, n_games, endgame_games, pieces


def compare_database_query(name, params):
    min_elo = int(params["minelo"])
    max_elo = int(params["maxelo"])
    games = Games.objects.filter(((Q(white__ne=name) & Q(white_elo__gte=min_elo) & Q(white_elo__lte=max_elo)) |
                                 (Q(black__ne=name) & Q(black_elo__gte=min_elo) & Q(black_elo__lte=max_elo))) &
                                 Q(five_piece_endgame_fen__ne=""))
    return games


def check_endgame_params(params):
    if "pieces" in params.keys():
        pieces = int(params["pieces"])
    else:
        pieces = 10
    from_date, to_date, min_elo, max_elo, opponent = check_params(params)
    return pieces, from_date, to_date, min_elo, max_elo, opponent


# only 6.6% of matches would end in the endgame (7983 out of 121114) (5 pieces or fewer)
# only 12% of matches would end in the endgame (14528 out of 121114) (7 pieces or fewer)
# only 22% of matches would end in the endgame (26618 out of 121114) (10 pieces or fewer)
def find_endgame_matches(n, games):
    j = 0
    h = 0
    pieces = "rnbqkp"
    result = []
    if n == 5:
        for game in games:
            if game.five_piece_endgame_fen != "":
                result.append((game, game.five_piece_endgame_fen))
                j += 1
            h += 1
    else:
        for game in games:
            i = 0
            pgn = io.StringIO(game.moves)
            parsed_game = chess.pgn.read_game(pgn)
            fen = parsed_game.end().board().board_fen().lower()
            for char in fen:
                if char in pieces:
                    i += 1
                if i > n:
                    break
            if i <= n:
                j += 1
                result.append((game, parsed_game))
            h += 1
    return j, h, result


# returns true if you have material advantage, false otherwise
def material_advantage(n, parsed_game, side):
    white = 0
    black = 0
    pieces = "rnbqkp"
    if n == 5:
        board = Board(parsed_game)
    else:
        board = endgame_start_board(n, parsed_game.end())
    for char in board.board_fen():
        if char in pieces:
            black += 1
        if char in pieces.upper():
            white += 1
    if side:
        return white > black
    else:
        return black > white


# returns 1 if you should win, -1 if you should lose and 0 if you should draw
def tablebase_evaluation(tb, parsed_game, n, side):
    if n == 5:
        board = Board(parsed_game)
    else:
        board = endgame_start_board(n, parsed_game.end())
    if not board.castling_rights:
        res = tb.probe_wdl(board)
        if res > 0:
            if board.turn == side:
                return 1
            else:
                return -1
        if res < 0:
            if board.turn == side:
                return -1
            else:
                return 1
        if res == 0:
            return 0
    else:
        return 2


def endgame_start_board(n, parsed_game):
    pieces = "rnbqkp"
    while True:
        i = 0
        fen = parsed_game.board().board_fen().lower()
        for char in fen:
            if char in pieces:
                i += 1
        if i > n:
            end_game_start = parsed_game.variations[0]
            break
        parsed_game = parsed_game.parent
    return end_game_start.board()
