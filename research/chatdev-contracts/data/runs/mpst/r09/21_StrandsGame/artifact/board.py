'''
board.py — board utilities for the "Strands" word-segmentation puzzle.
Provides:
- Cell: a lightweight (col, row) coordinate on the game board.
- parse_cell: safely converts player input like "B3" into a Cell, rejecting
  any out-of-bounds reference (e.g., "A0", "I2", "A99") so invalid input can
  never corrupt game state via negative-index wraparound or crash the
  interactive game loop with an IndexError.
- cell_name: converts a Cell back into its human-readable name.
- cells_adjacent: 8-directional adjacency test (Chebyshev distance 1),
  matching NYT Strands drag rules where diagonal moves are allowed.
board.py owns the board dimensions: 8 columns (A-H) via COL_LETTERS and
BOARD_ROWS rows. All other modules must derive grid size from these
constants so they can never fall out of sync.
'''
from collections import namedtuple
Cell = namedtuple("Cell", ["col", "row"])
COL_LETTERS = "ABCDEFGH"
BOARD_ROWS = 6  # grid height; board.py owns the board dimensions
def parse_cell(text):
    """Parse a cell reference like 'B3' into a Cell.
    Returns a Cell(col, row) with 0-based indices, or None if the text
    is not a valid in-bounds reference (e.g., 'A0', 'I2', 'A99').
    """
    text = text.strip().lower()
    if len(text) < 2 or len(text) > 3:
        return None
    col = COL_LETTERS.find(text[0])
    if col < 0:
        return None
    if not text[1:].isdigit():
        return None
    row = int(text[1:]) - 1
    if not (0 <= row < BOARD_ROWS):  # reject 'A0' (row=-1) and out-of-range rows
        return None
    return Cell(col, row)
def cell_name(cell):
    """Return the human-readable name (e.g., 'B3') for a Cell."""
    return f"{COL_LETTERS[cell.col]}{cell.row + 1}"
def cells_adjacent(a, b):
    """Return True if cells a and b are adjacent (8-directional, Chebyshev
    distance 1); same-cell is excluded since its distance is 0."""
    return max(abs(a.col - b.col), abs(a.row - b.row)) == 1