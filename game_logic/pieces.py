class Piece:
    def __init__(self, color, position):
        self.color = color
        self.position = position # y,x
        self.has_moved = False

    def can_move_to(self, new_position, board):
        # Implement how a piece moves
        return False

    def get_valid_moves(self, game, color):
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.color is color and self.can_move_to((row, col), game.board) and game.board.is_move_valid(self.position, (row,col), self.color):
                    valid_moves.append((row, col))
        return valid_moves

    def is_same_color_turn(self, game):
        return self.color == game.current_turn

    def __str__(self):
        return f'{self.color[0]}{self.__class__.__name__[0]}'

# Define specific piece classes like Pawn, Rook, Knight, etc.
# These classes should inherit from Piece and implement specific movement rules.

class Pawn(Piece):
    def __str__(self):
        return super().__str__().lower()

    def can_move_to(self, new_position, board):
        dx = new_position[1] - self.position[1]
        dy = new_position[0] - self.position[0]
        forward = 1 if self.color == 'white' else -1
        start_row = 1 if self.color == 'white' else 6

        # Forward move
        if dx == 0:
            if (self.position[0] == start_row and dy == 2 * forward and
                board.get_piece((self.position[0] + forward, self.position[1])) is None and
                board.get_piece(new_position) is None):
                return True
            if dy == forward and board.get_piece(new_position) is None:
                return True

        # Capture move
        elif abs(dx) == 1 and dy == forward:
            target_piece = board.get_piece(new_position)
            if target_piece is not None and target_piece.color != self.color:
                return True

        # En passant capture logic
        if abs(dx) == 1 and dy == forward:
            target_piece = board.get_piece(new_position)
            if target_piece is None:
                # Check if en passant is possible
                beside_piece = board.get_piece((self.position[0],  new_position[1]))
                if isinstance(beside_piece, Pawn) and beside_piece.color != self.color:
                    last_move = board.last_move
                    if last_move and last_move[0] == beside_piece:
                        move_diff = abs(last_move[2][0] - last_move[1][0])
                        if move_diff == 2:
                            # En passant condition met
                            return True

        return False

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.has_moved = False

    def move_like_rook(self, new_position, board):
        if not new_position or not self.position:
            return False  # Invalid positions

        dx = new_position[1] - self.position[1]
        dy = new_position[0] - self.position[0]

        target_piece = board.get_piece(new_position)
        # Check path and final position
        if dx != 0 and dy == 0:  # Horizontal movement
            step = 1 if dx > 0 else -1
            for x in range(self.position[1] + step, new_position[1], step):
                if board.get_piece((self.position[0], x)) is not None:
                    return False
            # Check the target square
            return target_piece is None or target_piece.color != self.color
        elif dy != 0 and dx == 0:  # Vertical movement
            step = 1 if dy > 0 else -1
            for y in range(self.position[0] + step, new_position[0], step):
                if board.get_piece((y, self.position[1])) is not None:
                    return False
            # Check the target square
            return target_piece is None or target_piece.color != self.color

        return False

    def can_move_to(self, new_position, board):
        return self.move_like_rook(new_position, board)

class Knight(Piece):
    def __str__(self):
        return f'{self.color[0]}{self.__class__.__name__[1].upper()}'

    def can_move_to(self, new_position, board):
        if not new_position or not self.position:
            return False  # Invalid positions

        dx = abs(new_position[1] - self.position[1])
        dy = abs(new_position[0] - self.position[0])
        target_piece = board.get_piece(new_position)
        return (dx, dy) in [(1, 2), (2, 1)] and (target_piece is None or target_piece.color != self.color)

class Bishop(Piece):
    def move_like_bishop(self, new_position, board):
        if not new_position or not self.position:
            return False  # Invalid positions

        dx = new_position[1] - self.position[1]
        dy = new_position[0] - self.position[0]

        if abs(dx) != abs(dy):  # Bishop moves only diagonally
            return False

        step_x = 1 if dx > 0 else -1
        step_y = 1 if dy > 0 else -1

        x, y = self.position[1], self.position[0]
        while (x, y) != (new_position[1] - step_x, new_position[0] - step_y):
            x += step_x
            y += step_y
            if board.get_piece((y,x)) is not None:
                return False

        target_piece = board.get_piece(new_position)
        return target_piece is None or target_piece.color != self.color

    def can_move_to(self, new_position, board):
        return self.move_like_bishop(new_position, board)


class Queen(Piece):
    def can_move_to(self, new_position, board):
        # Create instances of Rook and Bishop for movement logic
        virtual_rook = Rook(self.color, self.position)
        virtual_bishop = Bishop(self.color, self.position)

        # Check if the queen moves like a rook or a bishop
        if new_position[1] == self.position[1] or new_position[0] == self.position[0]:
            return virtual_rook.move_like_rook(new_position, board)
        elif abs(new_position[1] - self.position[1]) == abs(new_position[0] - self.position[0]):
            return virtual_bishop.move_like_bishop(new_position, board)
        else:
            return False


class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.has_moved = False

    def can_castle(self, new_position, board):
        if self.has_moved or new_position[0] != self.position[0]:
            return False

        rook_x = 0 if new_position[1] == 2 else 7
        rook = board.get_piece((self.position[0], rook_x))
        if not isinstance(rook, Rook) or rook.has_moved:
            return False

        # Check if squares between king and rook are empty and not under attack
        step = 1 if rook_x == 7 else -1
        for x in range(self.position[1] + step, rook_x, step):
            if board.get_piece((self.position[0], x)) is not None or \
            board.is_square_under_attack((self.position[0], x), 'black' if self.color == 'white' else 'white'):
                return False

        # Check if king's current position is under attack
        if board.is_in_check(self.color):
            return False

        return True

    def can_move_to(self, new_position, board):
        if not new_position or not self.position:
            return False  # Invalid positions

        if not self.has_moved and abs(new_position[1] - self.position[1]) == 2:
            return self.can_castle(new_position, board)

        dx = abs(new_position[1] - self.position[1])
        dy = abs(new_position[0] - self.position[0])
        target_piece = board.get_piece(new_position)
        return (dx in [0, 1] and dy in [0, 1]) and (target_piece is None or target_piece.color != self.color)
