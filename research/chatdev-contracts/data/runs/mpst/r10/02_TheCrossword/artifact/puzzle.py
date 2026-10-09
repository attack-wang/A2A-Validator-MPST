'''
puzzle.py — Puzzle data and layout logic for the crossword application.
Holds the solution grid and the across/down clues, and derives the
numbered word entries (position, direction, answer, clue) from the grid
so the game engine never hard-codes word positions by hand.
'''
# Solution grid: 5x5. '#' marks a black (blocked) square.
SOLUTION_GRID = [
    ['W', 'A', 'T', 'E', 'R'],
    ['A', '#', '#', '#', 'I'],
    ['V', '#', '#', '#', 'N'],
    ['E', '#', '#', '#', 'S'],
    ['S', 'T', 'O', 'N', 'E'],
]
ACROSS_CLUES = {
    1: "It falls as rain and fills the oceans (H2O)",
    3: "A small piece of rock",
}
DOWN_CLUES = {
    1: "Ocean movements that roll toward the shore",
    2: "Wash something lightly with water",
}
def _is_white(grid, r, c):
    """Return True if (r, c) is inside the grid and not a black square."""
    rows, cols = len(grid), len(grid[0])
    return 0 <= r < rows and 0 <= c < cols and grid[r][c] != '#'
def _run_length(grid, r, c, dr, dc):
    """Length of the white-cell run starting at (r, c) heading (dr, dc)."""
    n = 0
    while _is_white(grid, r + dr * n, c + dc * n):
        n += 1
    return n
def build_entries(grid=SOLUTION_GRID, across_clues=ACROSS_CLUES, down_clues=DOWN_CLUES):
    """Derive numbered across/down entries from the solution grid.
    Returns a list of dicts:
        {'number', 'direction' ('A'/'D'), 'row', 'col', 'length',
         'answer', 'clue'}
    Only runs of length >= 2 count as entries and receive clue numbers,
    exactly like real crossword numbering.
    """
    entries = []
    numbers = {}  # (row, col) -> clue number
    next_number = 1
    rows, cols = len(grid), len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if not _is_white(grid, r, c):
                continue
            starts_across = _run_length(grid, r, c, 0, 1) >= 2 and not _is_white(grid, r, c - 1)
            starts_down = _run_length(grid, r, c, 1, 0) >= 2 and not _is_white(grid, r - 1, c)
            if starts_across or starts_down:
                numbers[(r, c)] = next_number
                next_number += 1
    for r in range(rows):
        for c in range(cols):
            if not _is_white(grid, r, c):
                continue
            if _run_length(grid, r, c, 0, 1) >= 2 and not _is_white(grid, r, c - 1):
                n = numbers[(r, c)]
                length = _run_length(grid, r, c, 0, 1)
                entries.append({
                    'number': n, 'direction': 'A',
                    'row': r, 'col': c, 'length': length,
                    'answer': ''.join(grid[r][c + i] for i in range(length)),
                    'clue': across_clues[n],
                })
            if _run_length(grid, r, c, 1, 0) >= 2 and not _is_white(grid, r - 1, c):
                n = numbers[(r, c)]
                length = _run_length(grid, r, c, 1, 0)
                entries.append({
                    'number': n, 'direction': 'D',
                    'row': r, 'col': c, 'length': length,
                    'answer': ''.join(grid[r + i][c] for i in range(length)),
                    'clue': down_clues[n],
                })
    return entries