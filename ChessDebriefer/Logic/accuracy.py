import re
from mongoengine import Q
from ChessDebriefer.Logic.games import evaluate_game
from ChessDebriefer.models import Games


def calculate_accuracy(name):
    accuracy = 0
    total_moves = 0
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
    return round(((accuracy * 1.) / total_moves) * 100, 2)
