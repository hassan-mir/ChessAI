from game_logic.pieces import Pawn, Rook, Knight, Bishop, Queen, King

class Chessboard:
    def __init__(self):
        self.board = self.create_board()
        self.last_move = None
        self.en_passant_target = None

    """Board layout:

        7  bR bN bB bQ bK bB bN bR
        6  bp bp bp bp bp bp bp bp
        5  .  .  .  .  .  .  .  .
        4  .  .  .  .  .  .  .  .
        3  .  .  .  .  .  .  .  .
        2  .  .  .  .  .  .  .  .
        1  wp wp wp wp wp wp wp wp
        0  wR wN wB wQ wK wB wN wR
            0  1  2  3  4  5  6  7
    """


#board setup
    @staticmethod
    def create_board():
        """Initializes an 8x8 board with pieces in their starting positions."""
        board = [[None for _ in range(8)] for _ in range(8)]

        # Pawns
        for i in range(8):
            board[1][i] = Pawn('white', (1, i))
            board[6][i] = Pawn('black', (6, i))

        # Other pieces
        pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        #Test for stalemate
        #pieces = [None, None, None, Queen, King, None, None, None]
        for i, Piece in enumerate(pieces):
            if Piece:
                board[0][i] = Piece('white', (0, i))
                board[7][i] = Piece('black', (7, i))

        return board

    def reset_board(self):
        """Resets the board to its initial state."""
        self.board = self.create_board()

#move piece
    def move_piece_successful(self, old_position, new_position):
        """Attempts to move a piece and returns True if successful."""
        piece = self.get_piece(old_position)
        if piece and piece.can_move_to(new_position, self):
            piece = self.handle_special_moves(piece, old_position, new_position)
            self.handle_castling(piece, old_position, new_position)
            self.make_move(piece, old_position, new_position)
            return True
        return False

    def make_move(self, piece, old_position, new_position):
        """Moves a piece on the board and updates relevant properties."""
        self.set_piece(piece, new_position)
        self.set_piece(None, old_position)
        self.last_move = (piece, old_position, new_position)
        piece.has_moved = True

    def get_piece(self, position):
        """Returns the piece at the specified position."""
        return self.board[position[0]][position[1]]

    def set_piece(self, piece, position):
        """Sets a piece at the given position on the chessboard."""
        y, x = position
        self.board[y][x] = piece
        if piece and position is not piece.position:
            piece.position = position

    def try_move_piece(self, from_position, to_position, current_turn):
        if from_position == to_position:
            return False

        piece = self.get_piece(from_position)
        if piece and piece.color == current_turn:
            if self.get_piece(to_position) is not None and self.get_piece(to_position).color == current_turn:
                return False

            if not self.is_move_valid(from_position, to_position, current_turn):
                return False

            if self.move_piece_successful(from_position, to_position):
                return True

        return False

#special moves
    def handle_special_moves(self, piece, old_position, new_position):
        """Handles special moves like en passant and pawn promotion."""
        if isinstance(piece, Pawn):
            if abs(new_position[0] - old_position[0]) == 2:
                self.en_passant_target = new_position
                return piece
            elif self.en_passant_target and new_position[1] == self.en_passant_target[1]:
                captured_pawn_position = (old_position[0], new_position[1])
                self.set_piece(None, captured_pawn_position)
            self.en_passant_target = None

            if new_position[0] in [0, 7]:
                return self.promote(piece)

        return piece

    def promote(self, pawn):
        """Promotes a pawn to a queen."""
        self.set_piece(Queen(pawn.color, pawn.position), pawn.position)
        return self.get_piece(pawn.position)

    def handle_castling(self, piece, old_position, new_position):
        """Handles castling moves."""
        if isinstance(piece, King) and abs(new_position[1] - old_position[1]) == 2:
            rook_x = 0 if new_position[1] == 2 else 7
            rook_new_x = 3 if new_position[1] == 2 else 5
            rook = self.get_piece((old_position[0], rook_x))
            self.make_move(rook, (old_position[0], rook_x), (old_position[0], rook_new_x))

#check and end game scenarios
    def is_in_check(self, color):
        """Checks if opponent is in check."""
        king_position = self.find_king(color)
        return self.is_square_under_attack(king_position, 'black' if color == 'white' else 'white')

    def is_stalemate(self, game, color):
        """Checks if a player is in stalemate."""
        # If the player is in check, it's not stalemate.
        if self.is_in_check(color):
            return False

        # Check all pieces for the current player's color.
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                # If there's a piece of the player's color at this position...
                if piece and piece.color == color:
                    # Get all valid moves for this piece.
                    valid_moves = piece.get_valid_moves(game, color)
                    # Check each move to see if player can make move.
                    for move in valid_moves:
                        if self.is_move_valid((y, x), move, color):
                            # If any move puts the king in check it is stalemate.
                            return False

        # If no valid moves take the king out of check, it is checkmate.
        return True

    def is_checkmate(self, game, color):
        """Checks if a player is in checkmate."""
        # If the player is not in check, it's not checkmate.
        if not self.is_in_check(color):
            return False

        # Check all pieces for the current player's color.
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                # If there's a piece of the player's color at this position...
                if piece and piece.color == color:
                    # Get all valid moves for this piece.
                    valid_moves = piece.get_valid_moves(game, color)
                    # Check each move to see if it takes the king out of check.
                    for move in valid_moves:
                        if self.is_move_valid((y, x), move, color):
                            # If any valid move takes the king out of check, it's not checkmate.
                            return False

        # If no valid moves take the king out of check, it is checkmate.
        return True

#move validity checks and info
    def is_valid_position(self, position):
        """Checks if a position is within the board boundaries."""
        return 0 <= position[0] < 8 and 0 <= position[1] < 8

    def is_move_valid(self, from_position, to_position, color):
        """Checks if a move is valid without leaving the king in check."""
        # Temporarily make the move on the board
        original_piece = self.get_piece(to_position)
        moving_piece = self.get_piece(from_position)
        moving_piece_has_moved = moving_piece.has_moved
        current_last_move = self.last_move
        self.make_move(moving_piece, from_position, to_position)


        # Check if the king is in check
        in_check = self.is_in_check(color)

        # Revert the move and the has_moved status
        self.make_move(moving_piece, to_position, from_position)
        self.set_piece(moving_piece, from_position)
        self.set_piece(original_piece, to_position)
        moving_piece.position = from_position
        moving_piece.has_moved = moving_piece_has_moved
        self.last_move = current_last_move

        return not in_check

    def is_capture_move(self, piece, new_position):
            """Checks if a move is a capture move."""
            target_piece = self.get_piece(new_position)

            # Check if the move is an en passant capture
            if isinstance(piece, Pawn) and self.en_passant_target and new_position[1] == self.en_passant_target[1] and abs(piece.position[0] - self.en_passant_target[0]) == 0:
                return True

            return target_piece is not None and target_piece.color != piece.color

#helper methods
    def is_square_under_attack(self, position, attacker_color):
        """Checks if a square is under attack."""
        for row in self.board:
            for piece in row:
                if piece and piece.color == attacker_color:
                    if piece.can_move_to(position, self):
                        return True
        return False

    def find_king(self, color):
        """Finds and returns the position of the king with the specified color."""
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if isinstance(piece, King) and piece.color == color:
                    return (y, x)

        return None # If the king is not found, return None

    def print_board(self):
        """For testing: prints the board to the console."""
        for row in self.board:
            print(' '.join('. ' if piece is None else str(piece) for piece in row))