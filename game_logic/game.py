from game_logic.board import Chessboard


class Game:
    def __init__(self):
        self.board = Chessboard()
        self.current_turn = 'white'
        self.game_over = False
        self.is_stalemate = False
        self.is_checkmate = False
        self.is_current_player_in_check = False
        self.current_player_available_moves = []
        self.update_available_moves()

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

        self.update_available_moves()

        # Check for endgame conditions
        if self.board.is_in_check(self.current_turn):
            self.is_current_player_in_check = True
        else:
            self.is_current_player_in_check = False

        if self.board.is_checkmate(self, self.current_turn):
            self.game_over = True
            self.is_checkmate = True
        elif self.board.is_stalemate(self, self.current_turn):
            self.game_over = True
            self.is_stalemate = True

        return True # Return True if move succeeded

    def update_available_moves(self):
        """Updates list of all available moves for current player."""
        self.current_player_available_moves = []
        for y in range(8):
            for x in range(8):
                piece = self.board.get_piece((y, x))
                if piece and piece.color == self.current_turn:
                    valid_moves = piece.get_valid_moves(self, self.current_turn)
                    if valid_moves:
                        for move in valid_moves:
                            self.current_player_available_moves.append((piece.position, move))

    def get_available_moves(self):
        """Returns a list of all available moves for current player."""
        return self.current_player_available_moves

    def undo_move(self):
        """Undo the last move."""
        if self.board.history == [] or self.game_over:
            return
        self.board.undo_last_move(self.current_turn)
        self.switch_turn()

    def opposite_color(self, color):
        return 'black' if color == 'white' else 'white'

    def reset_game(self):
        self.board = Chessboard()
        self.current_turn = 'white'
        self.game_over = False
        self.is_stalemate = False
        self.is_checkmate = False

    def copy(self):
        """Returns a copy of the game."""
        copy = Game()
        copy.board = self.board.copy()
        copy.current_turn = self.current_turn
        copy.game_over = self.game_over
        copy.is_stalemate = self.is_stalemate
        copy.is_checkmate = self.is_checkmate
        copy.is_current_player_in_check = self.is_current_player_in_check
        copy.current_player_available_moves = self.current_player_available_moves
        return copy
