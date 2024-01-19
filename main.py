import random
import pygame
import sys
from ai.chess_ai import ChessAI
from ai.minimax.minimax_chess_ai import MinimaxChessAI
from ai.minimax.minimax_with_ab_pruning_chess_ai import MinimaxWithABPruningChessAI
from ai.random.random_chess_ai import RandomChessAI
from game_logic.game import Game
from gui.window import Window

def main():
    # Initialize Pygame
    pygame.init()

    # Decide which AI to use, None will mean both players are UI controlled
    ai_player = MinimaxWithABPruningChessAI(1)

    # Decide which color to play as
    #player_color = 'white'
    player_color = 'black'
    #player_color = random.choice(['white', 'black'])

    # Set up the game window
    window = Window(white_perspective = player_color == 'white', isAI=ai_player is not None)

    # Create an instance of the Game class
    game = Game()

    # Create a clock object to control the frame rate
    clock = pygame.time.Clock()

    # Main game loop
    running = True
    while running:
        # Handle events
        window.handle_events(game)

        # Render the current game state
        window.render(game)

        # If it's the AI's turn, make a move
        if not game.game_over and ai_player and game.current_turn != player_color:
            ai_move = ai_player.choose_move(game)
            if(ai_move is None):
                print('AI could not find a move')
                ai_player.choose_move(game)
            print('AI move was: ' + str(ai_move[0]) + '-->' + str(ai_move[1]))
            if(ai_move != None):
                if not game.attempt_move(ai_move[0], ai_move[1]):
                    raise Exception("AI made an invalid move:" + str(ai_move[0]) + '-->' + str(ai_move[1]) + '\n' + game.board.print_board())

        #for testing
        #game.board.print_board()

        # Render the current game state
        window.render(game)

        # Update display
        pygame.display.flip()

        # Limit the frame rate to 60 FPS
        clock.tick(60)

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()