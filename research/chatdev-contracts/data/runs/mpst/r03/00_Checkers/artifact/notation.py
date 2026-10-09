'''
notation.py
Parsing and formatting of player move notation.
Supported position formats:
  Algebraic:  b6, c5  (column letter a-h, row number 1-8, row 1 at bottom)
  Numeric:    3,2 or "3 2"  (row number 1-8, column number 1-8, a=1)
Supported move formats (from-to, optionally a jump chain):
  b6-c5
  b6 to c5
  b6-d4-f6          (multi-jump chain)
  3,2-4,3
  3,2 to 4,3
'''