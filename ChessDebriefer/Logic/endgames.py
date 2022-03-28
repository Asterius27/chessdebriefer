import io
import chess.pgn
from mongoengine import Q
from ChessDebriefer.models import Games


def calculate_endgame_percentages(name, params):
    wins = 0
    losses = 0
    draws = 0
    advantage = 0
    wins_adv = 0
    draws_adv = 0
    wins_disadv = 0
    draws_disadv = 0
    if "pieces" in params.keys():
        pieces = params["pieces"]
    else:
        pieces = 10
    games = Games.objects.filter(Q(white=name) | Q(black=name))
    n_endgame_games, n_games, endgame_games = find_endgame_matches(pieces, games)
    percentage_endgames = round((n_endgame_games / (n_games * 1.)) * 100, 2)
    for (game, parsed_game) in endgame_games:
        adv = material_advantage(pieces, parsed_game.end())
        if game.result == '1-0':
            if game.white == name:
                wins += 1
                if adv:
                    advantage += 1
                    wins_adv += 1
                else:
                    wins_disadv += 1
            if game.black == name:
                losses += 1
                if not adv:
                    advantage += 1
        if game.result == '0-1':
            if game.white == name:
                losses += 1
                if adv:
                    advantage += 1
            if game.black == name:
                wins += 1
                if not adv:
                    advantage += 1
                    wins_adv += 1
                else:
                    wins_disadv += 1
        if game.result == '1/2-1/2':
            draws += 1
            if game.white == name:
                if adv:
                    advantage += 1
                    draws_adv += 1
                else:
                    draws_disadv += 1
            if game.black == name:
                if not adv:
                    advantage += 1
                    draws_adv += 1
                else:
                    draws_disadv += 1
    return {'endgames': n_endgame_games,
            'percentage of games that finish in the endgame': percentage_endgames, 'wins': wins, 'losses': losses,
            'draws': draws, 'endgames with material advantage': advantage,
            'endgames without material advantage': n_endgame_games - advantage,
            'wins with material advantage': wins_adv,
            'losses with material advantage': advantage - (wins_adv + draws_adv),
            'draws with material advantage': draws_adv,
            'wins without material advantage': wins_disadv,
            'losses without material advantage': (n_endgame_games - advantage) - (wins_disadv + draws_disadv),
            'draws without material advantage': draws_disadv}


# only 6.6% of matches would end in the endgame (7983 out of 121114) (5 pieces or fewer)
# only 12% of matches would end in the endgame (14528 out of 121114) (7 pieces or fewer)
# only 22% of matches would end in the endgame (26618 out of 121114) (10 pieces or fewer)
def find_endgame_matches(n, games):
    j = 0
    h = 0
    pieces = "rnbqkp"
    result = []
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


def material_advantage(n, parsed_game):
    white = 0
    black = 0
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
    for char in end_game_start.board().board_fen():
        if char in pieces:
            black += 1
        if char in pieces.upper():
            white += 1
    return white > black

