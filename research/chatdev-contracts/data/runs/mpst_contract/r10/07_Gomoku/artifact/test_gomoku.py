"""Unit tests for Gomoku game logic."""

import unittest

from gomoku import BLACK, GomokuGame


class TestGomoku(unittest.TestCase):
    def test_horizontal_win(self):
        game = GomokuGame()
        for col in range(5):
            game.place_stone(7, col)
            if col < 4:
                game.place_stone(8, col)
        self.assertEqual(game.winner, BLACK)

    def test_vertical_win(self):
        game = GomokuGame()
        for row in range(5):
            game.place_stone(row, 3)
            if row < 4:
                game.place_stone(row, 4)
        self.assertEqual(game.winner, BLACK)

    def test_diagonal_win(self):
        game = GomokuGame()
        for i in range(5):
            game.place_stone(3 + i, 3 + i)
            if i < 4:
                game.place_stone(3 + i, 4 + i)
        self.assertEqual(game.winner, BLACK)

    def test_anti_diagonal_win(self):
        game = GomokuGame()
        for i in range(5):
            game.place_stone(10 - i, 3 + i)
            if i < 4:
                game.place_stone(10 - i, 4 + i)
        self.assertEqual(game.winner, BLACK)

    def test_invalid_move(self):
        game = GomokuGame()
        game.place_stone(7, 7)
        with self.assertRaises(ValueError):
            game.place_stone(7, 7)
        with self.assertRaises(ValueError):
            game.place_stone(15, 0)

    def test_no_premature_win(self):
        game = GomokuGame()
        for col in range(4):
            game.place_stone(7, col)
            game.place_stone(8, col)
        self.assertIsNone(game.winner)


if __name__ == "__main__":
    unittest.main()