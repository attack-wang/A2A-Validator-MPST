'''
parser.py
Notation parsing and move-path validation.
Accepted input formats (case-insensitive):
  * single move:      "b6-a4", "b6 a4", "b6xa4", "b6 to a4"
  * multi-jump chain: "b6 d6 f4" (the full landing sequence)
A path is validated against a cloned board so the real game state is
never mutated during checking. Rules enforced here:
  * the path starts on the current player's piece (or on the piece
    that is mid-chain when a multi-jump is in progress);
  * every segment must be a legal move for that piece on the simulated
    board (mandatory capture applies to the first segment);
  * a multi-jump path may only be given while jumps are mandatory;
  * the path must stop as soon as the piece is crowned.
'''
import re
from board import BOARD_SIZE
from move import Move
from pieces import PieceColor
from rules import moves_for_piece, jump_targets
SQUARE_RE = re.compile(r'^([a-h])([1-8])$')
def parse_squares(text):
    """Parse user text into a list of (row, col) tuples, or None."""
    normalized = text.strip().lower()
    for sep in (' to ', 'x', ',', '-', '→'):
        normalized = normalized.replace(sep, ' ')
    tokens = normalized.split()
    if not tokens:
        return None
    positions = []
    for tok in tokens:
        m = SQUARE_RE.match(tok)
        if not m:
            return None
        col = ord(m.group(1)) - ord('a')
        row = int(m.group(2)) - 1
        positions.append((row, col))
    return positions