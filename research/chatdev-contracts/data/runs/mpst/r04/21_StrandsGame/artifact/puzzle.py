'''
puzzle.py
Defines the Puzzle class, which encapsulates a single Strands board:
a letter grid, a set of theme words, and a special spangram word.
A Puzzle knows how to:
  * report the letter at a given (row, col) cell
  * verify that a sequence of cells is a legal "strand" path
    (every consecutive pair of cells must be adjacent, cells unique)
  * spell the word produced by a path
  * classify a path as the spangram, a theme word, or neither
'''
class Puzzle:
    """A single Strands board: letter grid + theme words + spangram."""
    def __init__(self, name, theme, grid, theme_words, spangram, hint_text=""):
        """
        name        : str  - puzzle title
        theme       : str  - theme/hint shown to the player
        grid        : list[list[str]] - uppercase letters, grid[row][col]
        theme_words : list[str] - theme words (uppercase), excluding spangram
        spangram    : str - the special word that spans the board
        hint_text   : str - extra flavor text revealed with hints
        """
        self.name = name
        self.theme = theme
        self.grid = grid
        self.theme_words = [w.upper() for w in theme_words]
        self.spangram = spangram.upper()
        self.hint_text = hint_text
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows else 0
        self._validate_layout()
    # ------------------------------------------------------------------ #
    # Layout validation
    # ------------------------------------------------------------------ #
    def _validate_layout(self):
        """Sanity-check the board so a broken puzzle can never start."""
        if self.rows == 0 or any(len(row) != self.cols for row in self.grid):
            raise ValueError("Puzzle grid must be a non-empty rectangle.")
        for row in self.grid:
            for ch in row:
                if not (isinstance(ch, str) and len(ch) == 1 and ch.isalpha()):
                    raise ValueError("Grid cells must be single letters.")
        all_words = self.theme_words + [self.spangram]
        total_cells = self.rows * self.cols
        needed = sum(len(w) for w in all_words)
        if needed > total_cells:
            raise ValueError("Theme words need more cells than the grid has.")
        if len(set(all_words)) != len(all_words):
            raise ValueError("Duplicate word in puzzle definition.")
    # ------------------------------------------------------------------ #
    # Basic accessors
    # ------------------------------------------------------------------ #
    def letter_at(self, row, col):
        """Return the uppercase letter stored at (row, col)."""
        return self.grid[row][col].upper()
    def in_bounds(self, row, col):
        """True if (row, col) lies inside the grid."""
        return 0 <= row < self.rows and 0 <= col < self.cols
    def all_words(self):
        """Every target word: theme words plus the spangram."""
        return [self.spangram] + self.theme_words
    # ------------------------------------------------------------------ #
    # Path (strand) handling
    # ------------------------------------------------------------------ #
    @staticmethod
    def is_valid_path(path):
        """
        A path is a list of (row, col) tuples.
        Legal strand rules:
          * at least one cell
          * no cell repeated
          * every consecutive pair of cells is adjacent
            (8-directional: horizontal, vertical or diagonal)
        """
        if not path:
            return False
        seen = set()
        for cell in path:
            if cell in seen:
                return False
            seen.add(cell)
        for (r1, c1), (r2, c2) in zip(path, path[1:]):
            if max(abs(r1 - r2), abs(c1 - c2)) != 1:
                return False
        return True
    def word_for_path(self, path):
        """Spell out the word produced by walking the given path."""
        return "".join(self.letter_at(r, c) for r, c in path)
    def touches_opposite_sides(self, path):
        """
        True if the path touches a pair of opposite board edges
        (left+right or top+bottom) - the spangram requirement.
        """
        rows_touched = {r for r, _ in path}
        cols_touched = {c for _, c in path}
        left_right = 0 in cols_touched and (self.cols - 1) in cols_touched
        top_bottom = 0 in rows_touched and (self.rows - 1) in rows_touched
        return left_right or top_bottom
    # ------------------------------------------------------------------ #
    # Classification
    # ------------------------------------------------------------------ #
    def classify(self, word, path):
        """
        Classify a submitted strand.
        Returns one of:
          'spangram'      - the spangram, correctly spanning the board
          'spangram_short'- spangram letters but not touching opposite sides
          'theme'         - a valid theme word
          'non_theme'     - a real-ish word that is not part of the theme
          'invalid'       - not a target word at all
        """
        if word == self.spangram:
            if self.touches_opposite_sides(path):
                return "spangram"
            return "spangram_short"
        if word in self.theme_words:
            return "theme"
        return "non_theme" if len(word) >= 3 else "invalid"