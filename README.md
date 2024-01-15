# ChessAI: A Python Chess Game Using Pygame

ChessAI is a fully functional chess game written in Python using the Pygame library. It is designed to provide a complete chess playing experience, including all the standard rules and moves. The primary goal of ChessAI is to serve as a platform for experimenting with and learning machine learning concepts by creating various AI opponents.

## Features

- **Full Chess Game Logic**: Implements all standard chess rules, including special moves like castling, en passant, and pawn promotion.
- **Graphical User Interface**: Utilizes Pygame for rendering the chessboard and pieces, handling user input, and displaying game states.
- **Resizable Window**: The game window can be resized, and the layout will adjust accordingly to maintain a square aspect ratio.
- **Interactive Gameplay**: Players can move pieces by dragging and dropping with the mouse.
- **Endgame Scenarios**: The game detects and handles checkmate and stalemate conditions.

## Files Overview

1. `main.py`: The entry point of the application. Initializes the game and contains the main game loop.
2. `gui/window.py`: Defines the `Window` class for handling the graphical user interface.
3. `game_logic/`: Contains the game logic, including:
   - `pieces.py`: Definitions for each type of chess piece and their movement rules.
   - `board.py`: Manages the chessboard and handles moves, including special moves and game state checks.
   - `game.py`: Represents the overall game state and controls the game flow.
4. `test/test_game.py`: Contains unit tests for the game, ensuring the correctness of crucial game functionalities such as piece movements, special moves (e.g., castling, en passant, pawn promotion), and game state checks (e.g., check, checkmate, stalemate).

## How to Run

1. Install Python and Pygame.
2. Clone the repository or download the source files.
3. Run `main.py` to start the game.

## Next Steps: AI Implementation

The following are suggested methods for implementing AI opponents to play against:

1. **Minimax Algorithm with Alpha-Beta Pruning**: A classic approach for turn-based games like chess. It involves simulating future moves and choosing the best one.
2. **Monte Carlo Tree Search (MCTS)**: A more sophisticated method that uses random sampling of the game space to make decisions.
3. **Machine Learning-Based AI**: Using neural networks and reinforcement learning to train an AI. One famous example is Google's AlphaZero.
4. **Heuristic-Based AI**: An AI that uses specific chess strategies and heuristics to make decisions, useful for creating AI with varying difficulty levels.

## Conclusion

ChessAI offers a comprehensive platform for both chess enthusiasts and those interested in AI and machine learning. Whether you're looking to play a classic game of chess or to delve into AI development, ChessAI serves as an excellent starting point.
