'''
pieces.py
...
'''
RED = "red"
BLACK = "black"
BOARD_SIZE = 8
# Internal board coordinates are 0-indexed:
# row 0 is the bottom board row (display row "1"), row 7 is the top (display row "8").
# Red starts at the bottom (rows 0-2) and advances toward increasing rows;
# Black starts at the top (rows 5-7) and advances toward decreasing rows.
FORWARD_DELTAS = {
    RED: ((1, -1), (1, 1)),      # Red advances toward increasing rows (up the display)
    BLACK: ((-1, -1), (-1, 1)),  # Black advances toward decreasing rows (down the display)
}
ALL_DELTAS = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # kings may move in any diagonal direction
KING_ROW = {RED: BOARD_SIZE - 1, BLACK: 0}