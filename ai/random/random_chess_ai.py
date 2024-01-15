import random
from ai.chess_ai import ChessAI

class RandomChessAI(ChessAI):
    def choose_move(self, game):
        available_moves = game.get_available_moves()
        if available_moves:
            return random.choice(available_moves)
        else:
            return None
