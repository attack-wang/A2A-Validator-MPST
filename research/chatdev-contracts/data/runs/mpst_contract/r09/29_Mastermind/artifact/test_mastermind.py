"""Unit tests for Mastermind logic (run: python -m unittest test_mastermind)."""
import unittest
from game import parse_guess, score_guess, generate_secret


class TestMastermind(unittest.TestCase):
    def test_all_exact(self):
        self.assertEqual(score_guess(["R", "G", "B", "Y"], ["R", "G", "B", "Y"]), (4, 0))

    def test_all_partial(self):
        self.assertEqual(score_guess(["R", "G", "B", "Y"], ["Y", "B", "G", "R"]), (0, 4))

    def test_mixed(self):
        # secret R G B Y vs guess R B G G -> exact: R; partial: B, G
        self.assertEqual(score_guess(["R", "G", "B", "Y"], ["R", "B", "G", "G"]), (1, 2))

    def test_repeats(self):
        # secret R R G Y vs guess R R R R -> exact 2, partial 0
        self.assertEqual(score_guess(["R", "R", "G", "Y"], ["R", "R", "R", "R"]), (2, 0))

    def test_parse_valid(self):
        self.assertEqual(parse_guess("r,g b y"), ["R", "G", "B", "Y"])

    def test_parse_invalid(self):
        self.assertIsNone(parse_guess("R G B"))
        self.assertIsNone(parse_guess("R G B X"))

    def test_generate_secret(self):
        secret = generate_secret()
        self.assertEqual(len(secret), 4)
        for c in secret:
            self.assertIn(c, ("R", "G", "B", "Y", "O", "P"))


if __name__ == "__main__":
    unittest.main()