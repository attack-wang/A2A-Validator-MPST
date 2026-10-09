'''
display.py
Text rendering of the 8x8 checkers board with algebraic coordinates
(files a-h, ranks 1-8). Rank 8 is printed at the top and rank 1 at
the bottom, matching standard board orientation. Only dark squares
are playable; playable empty squares are shown as '.', light squares
as blanks.
'''
from board import BOARD_SIZE
FILES = 'abcdefgh'
def square_name(row, col):
    """Convert 0-based (row, col) to algebraic notation, e.g. (0, 0) -> 'a1'."""
    return f"{FILES[col]}{row + 1}"
def render(board):
    """Return the multi-line string picture of the board."""
    header = '    ' + '   '.join(FILES)
    separator = '  +' + '---+' * BOARD_SIZE
    lines = [header, separator]
    for rank in range(BOARD_SIZE, 0, -1):
        row = rank - 1
        cells = []
        for col in range(BOARD_SIZE):
            piece = board.get_piece(row, col)
            if piece is None:
                cells.append('.' if board.is_playable(row, col) else ' ')
            else:
                cells.append(piece.symbol)
        lines.append(f' {rank} | ' + ' | '.join(cells) + f' | {rank}')
        lines.append(separator)
    lines.append(header)
    return '\n'.join(lines)