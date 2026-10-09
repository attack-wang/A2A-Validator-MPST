from game import Game
from move import Move
from notation import parse_move
BANNER = """
==================================================
    C H E C K E R S   ( D R A U G H T S )
           ChatDev Console Edition
==================================================
  Red (r/R) moves first. Red moves UP the board
  (toward row 8); Black (b/B) moves DOWN (toward
  row 1). Captures are mandatory. Reach the far
  row to crown a King (K moves any direction).
==================================================
"""
HELP_TEXT = """
Commands:
  help      - show this help message
  board     - redraw the board
  resign    - resign the game (opponent wins)
  quit      - exit the program
Move notation (columns a-h left to right, rows 1-8 top to bottom):
  Algebraic:   b3-a4      simple diagonal move from b3 to a4
               c3xe5      jump/capture from c3 to e5
               (separators '-', 'x', 'to' or spaces are all accepted)
  Numeric:     3,2-4,3    move from display row 3, col 2 to row 4, col 3
Rules reminders:
  * Captures are mandatory: if a jump exists you must jump.
  * Multi-jumps: after a capture, if the same piece can jump again,
    you must keep jumping with that piece.
  * A piece that reaches the far row is crowned and may then move
    and capture in all four diagonal directions.
"""