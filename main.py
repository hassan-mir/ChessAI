import pygame
import sys
from game_logic.game import Game
from gui.window import Window

def main():
    # Initialize Pygame
    pygame.init()

    # Set up the game window
    window = Window(white_perspective=True)

    # Create an instance of the Game class
    game = Game()

    # Main game loop
    running = True
    while running:
        # Handle events
        window.handle_events(game)

        # Render the current game state
        window.render(game)

        #for testing
        #game.board.print_board()

        # Update display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()