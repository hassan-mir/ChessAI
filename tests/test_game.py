import unittest
import sys
sys.path.append('D:\\Projects\\ChessAI')
from game_logic.game import Game
from game_logic.pieces import Pawn, Queen, Rook, King
import os
# Compute the path to the root directory (ChessAI/) and adds it to sys.path. Allows for running tests from root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_invalid_move(self):
        # Trying to move pawn three spaces forward from its initial position
        result = self.game.attempt_move((1, 0), (4, 0))
        self.assertFalse(result)

    def test_castling(self):
        # Setup the board for castling and perform the move
        self.game.board.set_piece(None, (0, 1))  # Remove knight from its initial position
        self.game.board.set_piece(None, (0, 2))  # Remove bishop from its initial position
        self.game.board.set_piece(None, (0, 3))  # Remove queen from its initial position

        result = self.game.attempt_move((0, 4), (0, 2))  # Perform castling move

        self.assertTrue(result)
        should_be_king = self.game.board.get_piece((0, 2))
        should_be_rook = self.game.board.get_piece((0, 3))
        self.assertTrue(isinstance(should_be_king, King))  # Check if king is in the new position
        self.assertTrue(should_be_king.color == 'white')
        self.assertTrue(isinstance(should_be_rook, Rook))  # Check if rook is in the new position
        self.assertTrue(should_be_rook.color == 'white')
        self.assertEqual(self.game.current_turn, 'black')  # Check if turn has switched to black

    def test_en_passant(self):
        # Setup:
        self.game.board.set_piece(Pawn('black', (3, 3)), (3, 3))  # create black pawn two steps ahead of white pawns
        self.game.attempt_move((1, 4), (3, 4))  # White pawn moves two steps forward next to pawn

        # Check the setup
        self.assertIsNotNone(self.game.board.get_piece((3, 3)))
        self.assertIsNotNone(self.game.board.get_piece((3, 4)))

        # Perform en passant
        result = self.game.attempt_move((3, 3), (2, 4))  # Black pawn captures white pawn en passant

        # Check if en passant was successful
        self.assertTrue(result)
        self.assertIsNone(self.game.board.get_piece((3, 3)))  # The white pawn moved from its position
        self.assertIsNone(self.game.board.get_piece((3, 4)))  # The black pawn should be captured
        should_be_pawn = self.game.board.get_piece((2, 4))
        self.assertTrue(isinstance(should_be_pawn, Pawn)) # The white pawn should be below the black pawn's place
        self.assertTrue(should_be_pawn.color == 'black')

    def test_pawn_promotion(self):
        # Move a pawn to the last rank and test promotion
        self.game.board.set_piece(Pawn('white', (6, 0)), (6, 0)) # Create white pawn on the 2nd last rank
        self.game.board.set_piece(None, (7, 0)) # Remove the black rook from its initial position

        # Perform promotion
        result = self.game.attempt_move((6, 0), (7, 0))  # White pawn moves to last rank

        # Check if promotion was successful
        self.assertTrue(result)
        should_be_queen = self.game.board.get_piece((7, 0))
        self.assertTrue(isinstance(should_be_queen, Queen)) # The white pawn should be promoted to a Queen
        self.assertTrue(should_be_queen.color == 'white')

    def test_check_detection(self):
        self.clear_board()
        # Place the black king in check from a white rook
        self.game.board.set_piece(King('black', (0, 0)), (0, 0))  # Black king
        self.game.board.set_piece(Rook('white', (1, 0)), (1, 0))  # White rook

        self.assertTrue(self.game.board.is_in_check('black'))  # Black king should be in check

    def test_checkmate_detection(self):
        self.clear_board()
        # Setup a simple checkmate scenario
        self.game.board.set_piece(King('black', (0, 0)), (0, 0))  # Black king
        self.game.board.set_piece(Queen('white', (1, 1)), (1, 1))  # White queen
        self.game.board.set_piece(Rook('white', (1, 0)), (1, 0))  # White rook

        self.assertTrue(self.game.board.is_checkmate(self.game, 'black'))  # Black king should be in checkmate

    def test_stalemate_detection(self):
        self.clear_board()
        # Setup a simple stalemate scenario
        self.game.board.set_piece(King('black', (0, 0)), (0, 0))  # Black king
        self.game.board.set_piece(Queen('white', (2, 1)), (2, 1))  # White queen
        self.game.board.set_piece(King('white', (2, 0)), (2, 0))  # White king

        self.assertTrue(self.game.board.is_stalemate(self.game, 'black'))  # Black king should be in stalemate

    def test_piece_capture(self):
        self.game.current_turn = 'black'
        # Setup a scenario where a black pawn captures a white pawn
        self.game.board.set_piece(Pawn('white', (3, 0)), (3, 0))  # White pawn
        self.game.board.set_piece(Pawn('black', (4, 1)), (4, 1))  # Black pawn

        result = self.game.attempt_move((4, 1), (3, 0))  # Black pawn captures white pawn
        self.assertTrue(result)
        self.assertIsNone(self.game.board.get_piece((4, 1)))  # The black pawn has moved
        self.assertIsNotNone(self.game.board.get_piece((3, 0)))  # The black pawn has captured the white pawn
        self.assertTrue(isinstance(self.game.board.get_piece((3, 0)), Pawn))  # Ensure it's a pawn at the new position
        self.assertEqual(self.game.board.get_piece((3, 0)).color, 'black')  # Ensure the pawn is black

    def test_turn_switching(self):
        self.game.attempt_move((1, 0), (2, 0))  # Pawn move
        self.assertEqual(self.game.current_turn, 'black')

    def clear_board(self):
        for i in range(8):
            for j in range(8):
                self.game.board.set_piece(None, (i, j))

if __name__ == '__main__':
    unittest.main()
