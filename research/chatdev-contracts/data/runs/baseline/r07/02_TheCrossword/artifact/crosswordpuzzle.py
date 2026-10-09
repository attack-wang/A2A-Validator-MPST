import sys
class CrosswordPuzzle:
    """Represents the crossword grid, its clues and the current game state."""
    def __init__(self):
        # ----------------------------------------------------------
        # Solution grid: '#' marks a black (blocked) square, letters
        # mark the white squares that belong to the answer words.
        # ----------------------------------------------------------
        self.solution = [
            ['S', 'U', 'N', '#', '#'],
            ['#', '#', 'O', '#', '#'],
            ['S', 'N', 'O', 'W', 'Y'],
            ['E', '#', 'O', '#', 'E'],
            ['A', 'M', 'A', 'S', 'S'],
        ]
        self.rows = len(self.solution)
        self.cols = len(self.solution[0])
        # Current board state: '' = empty white square, '#' = block.
        self.board = [
            [ch if ch == '#' else '' for ch in row] for row in self.solution
        ]
        # ----------------------------------------------------------
        # Word entries: clue number, direction, start cell, answer
        # and the clue text shown to the player.
        # ----------------------------------------------------------
        self.entries = [
            {"number": 1, "direction": "across", "row": 0, "col": 0,
             "answer": "SUN", "clue": "Star that lights our day"},
            {"number": 2, "direction": "down", "row": 0, "col": 2,
             "answer": "NOON", "clue": "Twelve o'clock, midday"},
            {"number": 3, "direction": "across", "row": 2, "col": 0,
             "answer": "SNOWY", "clue": "Covered with winter flakes"},
            {"number": 3, "direction": "down", "row": 2, "col": 0,
             "answer": "SEA", "clue": "Vast body of salt water"},
            {"number": 4, "direction": "down", "row": 2, "col": 4,
             "answer": "YES", "clue": "Affirmative reply"},
            {"number": 5, "direction": "across", "row": 4, "col": 0,
             "answer": "AMASS", "clue": "Pile up, as a fortune"},
        ]
        # Fast lookup table: (number, direction) -> entry dict.
        self.lookup = {(e["number"], e["direction"]): e for e in self.entries}
    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------
    def display_grid(self):
        """Print the current grid; clue numbers mark word-start cells."""
        start_numbers = {(e["row"], e["col"]): e["number"] for e in self.entries}
        print("\nCurrent grid  ('#' = black square, '_' = empty square):\n")
        for r in range(self.rows):
            cells = []
            for c in range(self.cols):
                if self.solution[r][c] == '#':
                    cells.append(" ## ")
                else:
                    letter = self.board[r][c] or "_"
                    num = start_numbers.get((r, c))
                    label = "{0}{1}".format(num, letter) if num else " {0} ".format(letter)
                    cells.append(" {0} ".format(label))
            print("".join(cells))
        print()