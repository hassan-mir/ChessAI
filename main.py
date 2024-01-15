import random
import pygame
import sys
from ai.chess_ai import ChessAI
from ai.random.random_chess_ai import RandomChessAI
from game_logic.game import Game
from gui.window import Window

def main():
    # Initialize Pygame
    pygame.init()

    # Decide which AI to use, None will mean both players are UI controlled
    ai_player = RandomChessAI()

    # Decide which color to play as
    #player_color = 'white'
    #player_color = 'black'
    player_color = random.choice(['white', 'black'])

    # Set up the game window
    window = Window(white_perspective = player_color == 'white')

    # Create an instance of the Game class
    game = Game()

    # Create a clock object to control the frame rate
    clock = pygame.time.Clock()

    # Main game loop
    running = True
    while running:
        # Handle events
        window.handle_events(game)

        # If it's the AI's turn, make a move
        if ai_player and game.current_turn != player_color:
            ai_move = ai_player.choose_move(game)
            if(ai_move != None):
                game.attempt_move(ai_move[0], ai_move[1])

        # Render the current game state
        window.render(game)

        #for testing
        #game.board.print_board()

        # Update display
        pygame.display.flip()

        # Limit the frame rate to 60 FPS
        clock.tick(60)

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()