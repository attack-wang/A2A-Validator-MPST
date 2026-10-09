"""Unit tests for the tic-tac-toe game logic."""

import unittest

from game import TicTacToe


class TestTicTacToe(unittest.TestCase):
    def test_initial_state(self):
        game = TicTacToe()
        self.assertEqual(game.current_player, "X")
        self.assertFalse(game.is_over())

    def test_valid_and_invalid_moves(self):
        game = TicTacToe()
        self.assertTrue(game.make_move(5))
        self.assertFalse(game.make_move(5))   # occupied
        self.assertFalse(game.make_move(0))   # out of range
        self.assertFalse(game.make_move(10))  # out of range
        self.assertFalse(game.make_move(None))

    def test_turn_alternation(self):
        game = TicTacToe()
        game.make_move(1)
        game.switch_player()
        self.assertEqual(game.current_player, "O")
        game.switch_player()
        self.assertEqual(game.current_player, "X")

    def test_row_win(self):
        game = TicTacToe()
        for pos in (1, 4, 2, 5, 3):
            game.make_move(pos)
            game.switch_player()
        self.assertEqual(game.check_winner(), "X")
        self.assertEqual(game.winning_line(), (1, 2, 3))
        self.assertTrue(game.is_over())

    def test_diagonal_win(self):
        game = TicTacToe()
        for pos in (1, 2, 5, 3, 9):
            game.make_move(pos)
            game.switch_player()
        self.assertEqual(game.check_winner(), "X")

    def test_draw(self):
        game = TicTacToe()
        for pos in (1, 2, 5, 3, 6, 4, 7, 9, 8):
            game.make_move(pos)
            game.switch_player()
        self.assertIsNone(game.check_winner())
        self.assertTrue(game.is_full())
        self.assertTrue(game.is_over())


if __name__ == "__main__":
    unittest.main()