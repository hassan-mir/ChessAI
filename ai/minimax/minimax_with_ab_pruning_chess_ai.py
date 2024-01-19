from ai.chess_ai import ChessAI
from game_logic.pieces import Bishop, King, Knight, Pawn, Queen, Rook
from game_logic.game import Game

class MinimaxWithABPruningChessAI(ChessAI):
    def __init__(self, depth=3):
        # Initialize the AI with a specified search depth
        self.depth = depth

    def choose_move(self, game: Game):
        # Choose the best move based on the Minimax algorithm
        # Make a copy of the game to avoid altering the original game state

        game = game.copy()
        return self.get_minimax_best_move(game)

    def get_minimax_best_move(self, game: Game):
        # Determines the best move by iterating over possible moves and applying the Minimax algorithm
        best_move = None
        best_score = float('-inf')
        for move in game.get_available_moves():
            game.attempt_move(move[0], move[1])
            score = self.minimax(game, self.depth, False, float('-inf'), float('inf'))
            game.undo_move()
            if score >= best_score:
                best_move = move
                best_score = score
        return best_move

    def minimax(self, game: Game, depth, maximizing_player, alpha, beta):
        # The Minimax algorithm: recursively calculates the best score for the current player
        if depth == 0 or game.game_over:
            # Base case: return the evaluated score if the depth is zero or the game is over
            return self.evaluate(game)

        if maximizing_player:
            # Maximizing player: tries to get the highest possible score
            best_score = float('-inf')
            for move in game.get_available_moves():
                game.attempt_move(move[0], move[1])
                score = self.minimax(game, depth - 1, False, alpha, beta)
                game.undo_move()
                best_score = max(best_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return best_score
        else:
            # Minimizing player: tries to minimize the opponent's score
            best_score = float('inf')
            for move in game.get_available_moves():
                game.attempt_move(move[0], move[1])
                score = self.minimax(game, depth - 1, True, alpha, beta)
                game.undo_move()
                best_score = min(best_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return best_score

    def evaluate(self, game: Game):
        # Evaluate the board: a simple heuristic to score the board position
        if game.game_over:
            # Check for endgame conditions
            if game.is_checkmate:
                # Assign a high positive/negative score for checkmate
                return float('-inf') if game.current_turn == 'white' else float('inf')
            else:
                # Return 0 for a draw
                return 0
        else:
            # Calculate and return the score based on the pieces on the board
            white_score = 0
            black_score = 0
            for piece in game.board.get_all_pieces():
                if piece.color == 'white':
                    white_score += self.get_piece_value(piece)
                else:
                    black_score += self.get_piece_value(piece)
            return white_score - black_score


    def get_piece_value(self, piece):
        # Assigns values to chess pieces based on their importance and capabilities
        if isinstance(piece, Pawn):
            return 1
        elif isinstance(piece, Knight):
            return 3
        elif isinstance(piece, Bishop):
            return 3
        elif isinstance(piece, Rook):
            return 5
        elif isinstance(piece, Queen):
            return 9
        elif isinstance(piece, King):
            # King has an arbitrarily high value since losing the king means losing the game
            return 100
        else:
            # Handle unknown piece types
            raise ValueError('Unknown piece type: {}'.format(piece.get_type()))
