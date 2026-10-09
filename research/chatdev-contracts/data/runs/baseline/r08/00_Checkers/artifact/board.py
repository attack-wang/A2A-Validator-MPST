from piece import Piece
class Board:
    SIZE = 8
    COLS = 'abcdefgh'
    def __init__(self):
        self.grid = [[None] * 8 for _ in range(8)]
        self.setup()
    def setup(self):
        # Black on rows 0-2, dark squares
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = Piece('B')
        # Red on rows 5-7
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = Piece('R')
    def get_piece(self, row, col):
        return self.grid[row][col]
    def is_inside(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8
    def is_playable(self, row, col):
        return (row + col) % 2 == 1
    def remove_piece(self, row, col):
        self.grid[row][col] = None
    def display(self):
        lines = []
        lines.append('      a   b   c   d   e   f   g   h')
        sep = '   +' + '---+' * 8
        lines.append(sep)
        for r in range(8):
            disp_row = 8 - r
            cells = []
            for c in range(8):
                p = self.grid[r][c]
                if p:
                    cells.append(p.get_symbol())
                elif (r + c) % 2 == 1:
                    cells.append('.')
                else:
                    cells.append(' ')
            row_str = '  ' + f'{disp_row} ' + '|' + '|'.join(f' {ch} ' for ch in cells) + '|'
            lines.append(row_str)
            lines.append(sep)
        return '\n'.join(lines)