class CrosswordPuzzle:
    BLOCKED = '#'
    EMPTY = ' '
    def __init__(self, solution, clues):
        self.solution = [list(row) for row in solution]  # or accept list of lists
        self.height = len(self.solution)
        self.width = len(self.solution[0])
        self.clues = clues
        self.user_grid = [[cell if cell == self.BLOCKED else self.EMPTY for cell in row] for row in self.solution]
        self.entries = self._build_entries()
    def _build_entries(self):
        """Scan grid, assign numbers, build entry dicts."""
        ...
    def display(self):
        """Print grid with column indices and row numbers."""
        ...
    def display_clues(self):
        ...
    def get_entry(self, number, direction):
        ...
    def place_word(self, number, direction, guess):
        """Validate and place. Returns (ok, message)."""
        ...
    def check_entries(self):
        """Report status of each entry."""
        ...
    def is_complete(self):
        """user_grid == solution"""
        ...
    def reveal_answer(self, number, direction):
        """Fill in the correct answer for an entry."""
        ...