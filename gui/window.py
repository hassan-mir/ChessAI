import pygame

# Define the Button class
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
        font = pygame.font.SysFont(None, 24)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        window.blit(text, text_rect)


import sys
from utils.utilities import load_png_keep_aspect_ratio
from game_logic.pieces import King

class Window:
    def __init__(self, width=1028, height=1088, white_perspective=False, isAI=False):
        self.width = width
        self.height = height
        self.top_panel_height = 60
        self.block_size = self.width // 8  # Size of a single square
        self.piece_size = int(self.block_size * 0.8)  # Scale the piece size to 80% of the block size
        self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("ChessAI")
        self.white_perspective = white_perspective
        self.isAI = isAI

        self.new_game_button = Button(10, 10, 100, 40, 'New Game', (200, 100, 100))
        self.undo_button = Button(120, 10, 100, 40, 'Undo', (200, 100, 100))

        self.dragging_piece = None
        self.dragging_from_pos = None
        self.dragging_piece_pos = None
        self.hovered_piece = None


        # Load resources such as images, fonts, etc.
        self.load_resources()

    def load_resources(self):
        """
        Load in piece images.
        """
        pieces = ['bp', 'bR', 'bN', 'bB', 'bQ', 'bK', 'wp', 'wR', 'wN', 'wB', 'wQ', 'wK']
        self.images = {piece: load_png_keep_aspect_ratio(f'gui/assets/pieces/PNGs/{piece}.png', self.piece_size) for piece in pieces}


    def render(self, game):
        # Clear the screen
        self.window.fill((255, 255, 255))  # Fill with white or any background color

        # Draw the chessboard
        self.draw_chessboard(game)

        # Draw the chess pieces
        self.draw_pieces(game)

         # Draw the buttons
        self.draw_buttons()

        # Highlight the available moves for the hovered piece
        if self.dragging_piece is not None:
            self.highlight_moves(game, self.dragging_piece)
        elif self.hovered_piece is not None:
            self.highlight_moves(game, self.hovered_piece)
        if game.is_stalemate:
            self.render_mate(game, "Stalemate. Draw!")
        if game.is_checkmate:
            winner_color = game.opposite_color(game.current_turn)[0].upper() + game.opposite_color(game.current_turn)[1:]
            self.render_mate(game, 'Checkmate. ' + winner_color + ' Win!')

        # Update display
        pygame.display.flip()


    def update_sizes(self):
        # Get the current size of the display surface
        current_width = pygame.display.get_surface().get_width()
        current_height = pygame.display.get_surface().get_height()

        # Check if the window has been resized
        if current_width != self.width or current_height != self.height:
            # Update the size to the larger of the two dimensions to maintain a square
            new_size = min(current_width, current_height)
            self.width = new_size
            self.height = new_size

            # Update the display mode
            self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

            # Update block and piece sizes
            self.block_size = self.width // 8
            self.piece_size = int(self.block_size * 0.8)

            # Reload resources if needed
            self.load_resources()

    def draw_buttons(self):
        # Draw buttons on the screen
        self.new_game_button.draw(self.window)
        self.undo_button.draw(self.window)

    def render_mate(self, game, text):
        font = pygame.font.SysFont(None, 72)
        text = font.render(text, True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2 - 50))

        self.window.blit(text, text_rect)

        # Draw the "New Game" button
        button_text = font.render('New Game', True, (255, 255, 255))
        button_rect = button_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        pygame.draw.rect(self.window, (200, 100, 100), button_rect.inflate(10, 10))  # Inflate to add padding
        self.window.blit(button_text, button_rect)

        # Check if the button is clicked
        if self.is_button_clicked(button_rect):
            game.reset_game()

    def is_button_clicked(self, button_rect):
        # Check if the mouse click is within the button rectangle
        click = pygame.mouse.get_pressed()
        if click[0] == 1:  # Left mouse button
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                return True
        return False

    def draw_chessboard(self, game):
        # Draw the chessboard grid based on the player's perspective
        for row in range(8):
            for col in range(8):
                color = (255, 255, 255) if (row + col) % 2 == 0 else (100, 100, 100)
                x_pos = col * self.block_size
                y_pos = row * self.block_size + self.top_panel_height
                if self.white_perspective:
                    x_pos = (7 - col) * self.block_size
                    y_pos = (7 - row) * self.block_size + self.top_panel_height
                pygame.draw.rect(self.window, color, (x_pos, y_pos, self.block_size, self.block_size))

    def draw_pieces(self, game):
        # Draw all pieces based on the player's perspective
        for row in range(8):
            for col in range(8):
                piece = game.board.get_piece((row, col))
                if piece is not None and (self.dragging_piece_pos is None or piece != self.dragging_piece):
                    piece_key = str(piece)
                    piece_image = self.images[piece_key]

                    row_view = row
                    col_view = 7 - col
                    # Flip the image if player_perspective is black
                    if self.white_perspective:
                        row_view = 7 - row
                        col_view = col
                    # Calculate the position to center the piece image in the square
                    x_pos = col_view * self.block_size + (self.block_size - self.piece_size) // 2
                    y_pos = row_view * self.block_size + (self.block_size - self.piece_size) // 2 + self.top_panel_height
                    self.window.blit(piece_image, (x_pos, y_pos))

                    # Highlight the king in red border if it's in check
                    if isinstance(piece, King) and piece.color is game.current_turn and game.is_current_player_in_check:
                        self.highlight_square((row_view, col_view), (255, 0, 0))

        # Draw the dragging piece at the cursor position
        if self.dragging_piece and self.dragging_piece_pos is not None:
            piece_key = str(self.dragging_piece)
            piece_image = self.images[piece_key]
            # Center the piece on the cursor while dragging
            x_pos, y_pos = self.dragging_piece_pos
            x_pos -= self.piece_size // 2
            y_pos -= self.piece_size // 2
            self.window.blit(piece_image, (x_pos, y_pos))

    def highlight_moves(self, game, piece):
        # Draw a small light green circle on each available move for the piece
        block_size = self.width // 8  # Size of a single square
        highlight_radius = block_size // 8  # Radius of the highlight circle
        for move in piece.get_valid_moves(game, game.current_turn):
            move_row, move_col = move
            move_col = 7 - move_col # fix due to pygame reference frame
            # Flip the move if player_perspective is black
            if self.white_perspective:
                move_row = 7 - move_row
                move_col = 7 - move_col
            center_x = move_col * block_size + block_size // 2
            center_y = move_row * block_size + block_size // 2 + self.top_panel_height
            color = (0, 255, 0)  # Default color is light green

            if game.board.is_capture_move(piece, move):
                color = (255, 0, 0)  # Change color to red if it's a capture move

            # Create a surface with per-pixel alpha
            highlight_surface = pygame.Surface((block_size, block_size), pygame.SRCALPHA)
            alpha = 128  # 50% transparency (0 is fully transparent, 255 is fully opaque)
            color_with_alpha = color + (alpha,)

            # Draw a semi-transparent circle on the surface
            pygame.draw.circle(highlight_surface, color_with_alpha, (block_size // 2, block_size // 2), highlight_radius)

            # Blit (copy) this surface onto the window at the desired position
            self.window.blit(highlight_surface, (center_x - block_size // 2, center_y - block_size // 2))


    def get_square_from_cursor(self, pos, game):
        x, y = pos
        #ensure always in bounds
        row = max(0, min((y - self.top_panel_height) // self.block_size, 7))
        col = 7 - max(0, min(x // self.block_size, 7))

        #translate square to player perspective
        if self.white_perspective:
            row = 7 - row
            col = 7 - col
        return (row, col)

#handle events

    def handle_events(self, game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif game.game_over:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_down(event.pos, game)
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_move(event.pos, game)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_up(event.pos, game)
            elif event.type == pygame.VIDEORESIZE:
                self.update_sizes()

    def handle_mouse_down(self, pos, game):
        row, col = self.get_square_from_cursor(pos, game)
        piece = game.board.get_piece((row, col))
        if piece and piece.color == game.current_turn:
            self.dragging_piece = piece
            self.dragging_from_pos = (row, col)

    def handle_mouse_move(self, pos, game):
        row, col = self.get_square_from_cursor(pos, game)
        piece = game.board.get_piece((row, col))
        if piece:
            self.hovered_piece = piece
        else:
            self.hovered_piece = None
        if self.dragging_piece:
            # Update piece's position for rendering
            self.dragging_piece_pos = pos

    def handle_mouse_up(self, pos, game):
        if self.dragging_piece:
            row, col = self.get_square_from_cursor(pos, game)
            if (row, col) != self.dragging_from_pos:
                game.attempt_move(self.dragging_from_pos, (row, col))
        self.dragging_piece = None
        self.dragging_piece_pos = None

        # Check if any button is clicked
        if self.new_game_button.rect.collidepoint(pos):
            game.reset_game()
        elif self.undo_button.rect.collidepoint(pos):
            game.undo_move()
            if(self.isAI):
                game.undo_move()

    def highlight_square(self, position, color, border=5):
        """Highlights king when in check."""
        row, col = position
        x_pos = col * self.block_size
        y_pos = row * self.block_size + self.top_panel_height
        pygame.draw.rect(self.window, color, (x_pos, y_pos, self.block_size, self.block_size), border)