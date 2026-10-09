'''
game_logic.py
Core match-3 game logic: board representation, match detection,
gravity, cascades, scoring, and level/move management.
This module contains no GUI code so it can be tested independently.
'''
import random
class Board:
    """Represents the match-3 game board and its rules."""
    def __init__(self, rows=8, cols=8, num_types=6, seed=None):
        self.rows = rows
        self.cols = cols
        self.num_types = num_types
        self.rng = random.Random(seed)
        self.grid = [[0] * cols for _ in range(rows)]
        self.fill_board()
    def fill_board(self):
        """Fill the board with random candies avoiding initial matches.
        Falls back to a full random fill + shuffle if constrained
        generation stalls (guards against tiny num_types)."""
        stalled = False
        for r in range(self.rows):
            for c in range(self.cols):
                placed = False
                for _ in range(50):  # bounded retries per cell
                    candy = self.rng.randint(1, self.num_types)
                    if not self._creates_match_at(r, c, candy):
                        self.grid[r][c] = candy
                        placed = True
                        break
                if not placed:
                    self.grid[r][c] = self.rng.randint(1, self.num_types)
                    stalled = True
        if stalled:
            # resolve any accidental matches / deadlocks caused by fallback
            while self.find_matches() or not self.has_possible_moves():
                self.shuffle()