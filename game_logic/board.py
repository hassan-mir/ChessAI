from game_logic.pieces import Pawn, Rook, Knight, Bishop, Queen, King

class Chessboard:
    def __init__(self):
        self.board = self.create_board()
        self.history = []

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
    def try_move_piece(self, old_position, new_position, current_turn):
        """Attempts to move a piece and returns True if successful."""
        #only external entry to class to move piece

        # Check if moving
        if old_position == new_position or not self.is_valid_position(new_position):
            return False

        # Check if the move is valid
        piece = self.get_piece(old_position)
        target_piece = self.get_piece(new_position)
        if piece is None:
            return False
        if piece and piece.color == current_turn:
            if target_piece is not None and target_piece.color == current_turn:
                return False

        original_piece = piece
        has_moved_before_move = piece.has_moved
        # Make the move
        if piece and piece.can_move_to(new_position, self):
            piece = self.handle_pawn_special_moves(piece, old_position, new_position)
            self.handle_castling(piece, old_position, new_position)
            self.make_move(piece, old_position, new_position)
            self.history.append((original_piece, target_piece, old_position, new_position, has_moved_before_move))

            # Check if the move leaves the king in check
            if not self.is_in_check(current_turn):
                return True

            # Undo the move if the king is left in check
            self.undo_last_move(current_turn)

        return False

    def make_move(self, piece, old_position, new_position):
        """Moves a piece on the board and updates relevant properties."""
        self.set_piece(piece, new_position)
        self.set_piece(None, old_position)
        piece.has_moved = True

    def undo_last_move(self, color):
        """Undoes the last move made."""
        if self.history:
            last_move = self.history.pop()
            piece, target_piece, old_position, new_position, has_moved = last_move
            #king moving 2 squares implies castling
            if isinstance(piece, King) and abs(new_position[1] - old_position[1]) == 2:
                self.undo_castling(new_position)
                piece.has_moved = False
            #pawn moved diagonally onto empty square implies en passant
            if isinstance(piece, Pawn) and abs(new_position[0] - old_position[0]) == 1 \
                and abs(new_position[1] - old_position[1]) == 1 and target_piece is None:
                self.undo_en_passant(piece, old_position, new_position)
            #pawn moved to last rank implies promotion
            if isinstance(piece, Pawn) and new_position[0] in [0, 7]:
                self.undo_promtion(piece, old_position, new_position)
            self.set_piece(piece, old_position)
            self.set_piece(target_piece, new_position)
            piece.has_moved = has_moved

    def undo_castling(self, king_position):
        """Undoes castling."""
        rook_original_x = 0 if king_position[1] == 2 else 7
        rook_current_x = 3 if king_position[1] == 2 else 5
        rook = self.get_piece((king_position[0], rook_current_x))
        self.set_piece(rook, (king_position[0], rook_original_x))
        self.set_piece(None, (king_position[0], rook_current_x))
        rook.has_moved = False

    def undo_en_passant(self, pawn, old_position, new_position):
        """Undoes en passant."""
        captured_pawn_y = 3 if new_position[0] == 2 else 4
        captured_pawn = self.history[-1][0]
        self.set_piece(captured_pawn,  (captured_pawn_y, new_position[1]))

    def undo_promtion(self, pawn, old_position, new_position):
        """Undoes promotion."""
        self.set_piece(pawn, old_position)
        self.set_piece(None, new_position)

    def get_piece(self, position):
        """Returns the piece at the specified position."""
        return self.board[position[0]][position[1]]

    def get_all_pieces(self):
        """Returns a list of all pieces on the board."""
        pieces = []
        for row in self.board:
            for piece in row:
                if piece:
                    pieces.append(piece)
        return pieces

    def set_piece(self, piece, position):
        """Sets a piece at the given position on the chessboard."""
        y, x = position
        self.board[y][x] = piece
        if piece:
            piece.position = position

#special moves
    def handle_pawn_special_moves(self, piece, old_position, new_position):
        """Handles special moves like en passant and pawn promotion."""
        if isinstance(piece, Pawn):
            # Check if the move is an en passant capture
            if(self.is_en_passant_move(piece, self.get_piece(new_position), new_position)) and abs(old_position[1] - new_position[1]) == 1:
                self.set_piece(None, self.history[-1][3])
                return piece

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

        # Check all moves for the current player's color.
        valid_moves = game.get_available_moves()
        if valid_moves != []:
            # If any move where king is not in check game continues.
            return False

        # If no valid moves and king is not in check, it is stalemate.
        return True

    def is_checkmate(self, game, color):
        """Checks if a player is in checkmate."""
        # If the player is not in check, it's not checkmate.
        if not self.is_in_check(color):
            return False

        # Check all moves for the current player's color.
        valid_moves = game.get_available_moves()
        if valid_moves != []:
            # If any valid move takes the king out of check, game continues.
            return False

        # If no valid moves and king is in check, it is checkmate.
        return True

    #move validity checks and info
    def is_valid_position(self, position):
        """Checks if a position is within the board boundaries."""
        return 0 <= position[0] < 8 and 0 <= position[1] < 8

    def is_in_check_after_move(self, from_position, to_position, color):
        """Checks if a move is valid without leaving the king in check."""
        # Temporarily make the move on the board
        if not self.try_move_piece(from_position, to_position, color):
            # If move not successful then king is in check or move invalid
            return True

        # Undo the move
        self.undo_last_move(color)

        return False

    def is_capture_move(self, piece, new_position):
            """Checks if a move is a capture move."""
            target_piece = self.get_piece(new_position)

            if self.is_en_passant_move(piece, target_piece, new_position):
                return True

            return target_piece is not None and target_piece.color != piece.color

    def is_en_passant_move(self, piece, target_piece, new_position):
        # Check if the move is an en passant capture
        if self.history:
            last_move_piece, last_move_target_piece, last_move_old_position, last_move_new_position, has_moved = self.history[-1]
            if target_piece is None and isinstance(piece, Pawn) and isinstance(last_move_piece, Pawn) \
                and abs(piece.position[1] - new_position[1]) == 1 \
                and piece.color != last_move_piece.color \
                and ((piece.position[0] == 3  and last_move_new_position[0] == 3) or (piece.position[0] == 4  and last_move_new_position[0] == 4))  \
                and abs(last_move_old_position[0] - last_move_new_position[0]) == 2 \
                and new_position[1] == last_move_new_position[1]:
                return True

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

    def copy(self):
        """Returns a copy of the board."""
        board_copy = Chessboard()
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece:
                    board_copy.board[y][x] = piece.copy()
                else:
                    board_copy.board[y][x] = None
        return board_copy