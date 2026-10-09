'''
renderer.py — Text rendering for the crossword application.
Draws the puzzle grid (with clue numbers, black squares and the player's
current letters) and prints the across/down clue lists and progress.
'''
def render_grid(grid_state, entries):
    """Return a multi-line string showing the grid and its state.
    grid_state: 2D list where each cell is a guessed letter (str) or
                '' for an unfilled white cell; black squares are '#'.
    entries:    list of entry dicts (used to place clue numbers).
    """
    rows, cols = len(grid_state), len(grid_state[0])
    # Map every cell that starts an entry (length >= 2) to its number.
    numbers = {}
    for entry in entries:
        numbers.setdefault((entry['row'], entry['col']), entry['number'])
    header = '    ' + ' '.join(f'  {c} ' for c in range(cols))
    ...