from game import EMPTY

COLS = 'abcdefgh'


def render(board, moves):
    print()
    print('    a b c d e f g h')
    for r in range(board.size):
        cells = []
        for c in range(board.size):
            v = board.grid[r][c]
            cells.append('*' if v == EMPTY and (r, c) in moves else v)
        print(f'  {r + 1} ' + ' '.join(cells))
    black, white = board.score()
    print(f'\nScore -> Black: {black}  White: {white}')


def parse_move(text):
    """Accept formats like 'd3', '3d', 'd 3', '3, d'. Return (row, col) or None."""
    row = col = None
    for ch in text.strip().lower():
        if ch.isdigit() and 1 <= int(ch) <= 8 and row is None:
            row = int(ch) - 1
        elif ch in COLS and col is None:
            col = COLS.index(ch)
    if row is None or col is None:
        return None
    return (row, col)