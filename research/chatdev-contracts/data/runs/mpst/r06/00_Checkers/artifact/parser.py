'''
parser.py
Parses player move input in common notations such as:
    c3-d4, c3 d4, c3 to d4, c3xe5, c3-e5-g7, c3 e5 g7
Squares use a letter for the column (a-h) and a digit for the row (1-8).
'''
import re
from board import BOARD_SIZE
SEPARATORS = r"(?:\s*(?:-|to|x|>|->|\s)\s*)"
def parse_square(token):
    '''Convert "c3" into (row, col) or raise ValueError.'''
    token = token.strip().lower()
    if len(token) != 2:
        raise ValueError(f"Invalid square '{token}'. Use column letter + row digit, e.g. 'c3'.")
    col_letter, row_digit = token[0], token[1]
    if not ('a' <= col_letter <= 'h'):
        raise ValueError(...)
    if not ('1' <= row_digit <= '8'):
        raise ValueError(...)
    col = ord(col_letter) - ord('a')
    row = int(row_digit) - 1
    return (row, col)
def parse_move(text):
    '''Parse a move string into a list of (row, col) waypoints.'''
    normalized = text.strip().lower()
    normalized = re.sub(r'\bto\b', ' ', normalized)
    tokens = re.split(r'[-x>:\s]+', normalized)
    tokens = [t for t in tokens if t]
    if len(tokens) < 2:
        raise ValueError("A move needs at least a 'from' and a 'to' square, e.g. 'c3-d4'.")
    return [parse_square(t) for t in tokens]