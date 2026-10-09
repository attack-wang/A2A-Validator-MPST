'''
test_game_logic.py
Unit tests for the Game2048 engine.
...
'''
import unittest
from game_logic import Game2048
class TestSlideAndMerge(unittest.TestCase):
    def test_slide_left_basic(self):
        g = Game2048()
        row, gained, moved = g._slide_and_merge_row([2, 0, 0, 0])
        self.assertEqual(row, [2, 0, 0, 0])
        self.assertEqual(gained, 0)
        self.assertFalse(moved)
    def test_merge_once(self):
        g = Game2048()
        row, gained, moved = g._slide_and_merge_row([2, 2, 2, 2])
        self.assertEqual(row, [4, 4, 0, 0])
        self.assertEqual(gained, 8)
        self.assertTrue(moved)
    def test_merge_order(self):
        g = Game2048()
        row, gained, moved = g._slide_and_merge_row([2, 2, 4, 0])
        self.assertEqual(row, [4, 4, 0, 0])
        self.assertEqual(gained, 4)
class TestDirections(unittest.TestCase):
    def _board(self, rows):
        g = Game2048()
        g.board = [list(r) for r in rows]
        g.game_over = False
        return g
    def test_move_down(self):
        # Regression test for the 'down' transform bug: the board must not
        # be rotated 180 degrees after a down move.
        g = self._board([[2, 0], [0, 0]])
        self.assertTrue(g.move('down'))
        self.assertEqual(g.get_board(), [[0, 0], [2, 0]])
    def test_move_up(self):
        g = self._board([[0, 0], [2, 0]])
        self.assertTrue(g.move('up'))
        self.assertEqual(g.get_board(), [[2, 0], [0, 0]])
    def test_move_left(self):
        g = self._board([[0, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        self.assertTrue(g.move('left'))
        self.assertEqual(g.get_board()[0], [2, 0, 0, 0])
    def test_move_right(self):
        g = self._board([[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        self.assertTrue(g.move('right'))
        self.assertEqual(g.get_board()[0], [0, 0, 0, 2])
    def test_down_merge(self):
        g = self._board([[2, 0], [2, 0]])
        self.assertTrue(g.move('down'))
        self.assertEqual(g.get_board(), [[0, 0], [4, 0]])
        self.assertEqual(g.get_score(), 4)