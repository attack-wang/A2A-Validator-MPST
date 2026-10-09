'''
constants.py
Shared constants for the Gomoku application: board dimensions,
stone colors, cell states, and rendering symbols.
'''
BOARD_SIZE = 15
EMPTY = None
BLACK = 'black'
WHITE = 'white'
SYMBOLS = {BLACK: '●', WHITE: '○'}
# Star (hoshi) points on a 15x15 board, as (row, col) 0-indexed
STAR_POINTS = ((3, 3), (3, 11), (11, 3), (11, 11), (7, 7))