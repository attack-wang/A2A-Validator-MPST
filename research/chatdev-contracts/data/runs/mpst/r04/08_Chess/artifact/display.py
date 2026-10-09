'''
display.py
Terminal rendering of the chess board...
'''
def render_board(board):
    lines = []
    lines.append('')
    for row in range(8):
        rank = 8 - row
        line = ' {} |'.format(rank)
        for col in range(8):
            piece = board.grid[row][col]
            cell = piece.symbol if piece else ' '
            line += ' {} |'.format(cell)
        lines.append(line)
        lines.append('  +---+---+---+---+---+---+---+---+')
    lines.append('    a   b   c   d   e   f   g   h')
    lines.append('')
    return '\n'.join(lines)