class StrandGrid:
    """Letter grid with found/hint cell state and ASCII rendering."""
    def __init__(self, rows=ROWS, cols=COLS):
        self.rows = rows
        self.cols = cols
        self.letters = [[None]*cols for _ in range(rows)]
        self.found = set()      # cells claimed by accepted merges
        self.spangram_cells = set()
        self.hints = set()      # cells revealed via hints
    def in_bounds(self, cell): ...
    def neighbors(self, cell): # 8-directional
    def letter_at(self, cell): ...
    def set_letter(self, cell, ch): ...
    def cells(self): # iterator of all cells
    def unfilled_count(self)
    def render(self) -> str
    def coord_name(self, cell) -> "A1"
    @staticmethod parse_coord(token) -> cell or None