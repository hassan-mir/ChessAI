from game_logic.board import Chessboard


class Game:
    def __init__(self):
        self.board = Chessboard()
        self.current_turn = 'white'
        self.game_over = False
        self.is_stalemate = False
        self.is_checkmate = False

    def switch_turn(self):
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

    def attempt_move(self, from_position, to_position):
        """
        Attempts to make a move from from_position to to_position.
        Switches turn if move is successful, checks for endgame conditions.
        Returns True if move is successful, False otherwise.
        """
        if not self.board.try_move_piece(from_position, to_position, self.current_turn):
            return False

        self.switch_turn()

        if self.board.is_checkmate(self, self.current_turn):
            self.game_over = True
            self.is_checkmate = True
        elif self.board.is_stalemate(self, self.current_turn):
            self.game_over = True
            self.is_stalemate = True

        return not self.game_over # Return True if game is not over

    def opposite_color(self, color):
        return 'black' if color == 'white' else 'white'

    def reset_game(self):
        self.board = Chessboard()
        self.current_turn = 'white'
        self.game_over = False
        self.is_stalemate = False
        self.is_checkmate = False