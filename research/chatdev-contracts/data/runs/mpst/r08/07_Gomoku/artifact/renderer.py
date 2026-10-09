'''
renderer.py
Console presentation layer for the Gomoku game: draws the board with
row/column labels (0-14) and prints game messages. Stone colors are
mapped to symbols: empty '.', black 'X', white 'O'.
'''
from board import EMPTY, BLACK, WHITE
STONE_SYMBOLS = {EMPTY: '.', BLACK: 'X', WHITE: 'O'}
class Renderer:
    '''Handles all console output for the Gomoku game.'''
    def render_board(self, board):
        '''Print the board grid with aligned coordinate labels.'''
        header = '    ' + ' '.join(f'{c:2d}' for c in range(board.size))
        print(header)
        for r in range(board.size):
            cells = ' '.join(
                f'{STONE_SYMBOLS[board.get_cell(r, c)]:>2s}'
                for c in range(board.size)
            )
            print(f'{r:2d}  {cells}')
        print()
    def show_message(self, message):
        '''Print a message line to the console.'''
        print(message)