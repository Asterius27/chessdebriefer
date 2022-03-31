import re
from mongoengine import Q
from ChessDebriefer.Logic.games import evaluate_game
from ChessDebriefer.models import Games, Openings


def calculate_accuracy(name):
    accuracy = 0
    total_moves = 0
    dictionary = {}
    games = Games.objects.filter(Q(white=name) | Q(black=name))
    for game in games:
        i = 0
        if not game.best_moves:
            evaluate_game(game)
        temp = game.moves.split(" ")
        pattern = re.compile(r'\.$')
        moves = list(filter(lambda m: not pattern.search(m), temp))
        if game.white == name:
            for (move, best_move) in zip(moves, game.best_moves):
                if i % 2 == 0:
                    if move == best_move:
                        accuracy = accuracy + 1
                    total_moves = total_moves + 1
                i = i + 1
        if game.black == name:
            for (move, best_move) in zip(moves, game.best_moves):
                if i % 2 != 0:
                    if move == best_move:
                        accuracy = accuracy + 1
                    total_moves = total_moves + 1
                i = i + 1
    dictionary["general accuracy"] = round(((accuracy * 1.) / total_moves) * 100, 2)
    dictionary["accuracy after opening"] = calculate_accuracy_post_opening(name)
    return dictionary


def calculate_accuracy_post_opening(name):
    accuracy = 0
    total_moves = 0
    games = Games.objects.filter(Q(white=name) | Q(black=name))
    for game in games:
        opening = Openings.objects.filter(Q(id=game.opening_id)).first()
        if not game.best_moves:
            evaluate_game(game)
        temp1 = opening.moves.split(" ")
        temp2 = game.moves.split(" ")
        pattern = re.compile(r'\.$')
        game_moves = list(filter(lambda m: not pattern.search(m), temp2))
        opening_moves = list(filter(lambda m: not pattern.search(m), temp1))
        i = len(opening_moves)
        if game.white == name:
            for j in range(len(opening_moves), len(game_moves)):
                if i % 2 == 0:
                    if game_moves[j] == game.best_moves[j]:
                        accuracy = accuracy + 1
                    total_moves = total_moves + 1
                i = i + 1
        if game.black == name:
            for j in range(len(opening_moves), len(game_moves)):
                if i % 2 != 0:
                    if game_moves[j] == game.best_moves[j]:
                        accuracy = accuracy + 1
                    total_moves = total_moves + 1
                i = i + 1
    return round(((accuracy * 1.) / total_moves) * 100, 2)
