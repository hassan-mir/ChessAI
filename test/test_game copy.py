import unittest
import sys
sys.path.append('D:\Projects\ChessAI')
from game_logic.game import Game

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        print(self.game.board.print_board())

    # Add more tests for other methods and game states
    def test_move_piece(self):
        # Print the board before the move
        print("Before move:")
        print(self.game.board.print_board())

        # Test moving a piece
        result = self.game.attempt_move((1, 0), (2, 0))
        self.assertTrue(result)

        # Print the board after the move
        print("After move:")
        print(self.game.board.print_board())

        # Test that the piece has been moved
        self.assertIsNone(self.game.board.get_piece((1, 0)))
        self.assertIsNotNone(self.game.board.get_piece((2, 0)))

if __name__ == '__main__':
    unittest.main()