'''
move_parser.py
Parses player move input in algebraic-like notation (e.g. "b3-c4", "c3 x e5")
and defines MoveError used for all move-validation failures.
'''
FILES = 'abcdefgh'
class MoveError(Exception):
    """Raised when a move cannot be parsed or violates the rules of checkers."""
    pass
def parse_square(token):
    if not isinstance(token, str):
        raise MoveError("Square must be text like 'b3'.")
    token = token.strip().lower()
    if len(token) != 2:
        raise MoveError(f"Invalid square '{token}': use file+rank, e.g. 'b3'.")
    file_ch, rank_ch = token[0], token[1]
    if file_ch not in FILES:
        raise MoveError(f"Invalid file '{file_ch}' in '{token}': use a-h.")
    if not rank_ch.isdigit():
        raise MoveError(f"Invalid rank '{rank_ch}' in '{token}': use 1-8.")
    col = ord(file_ch) - ord('a')
    row = int(rank_ch) - 1
    if not (0 <= row < 8):
        raise MoveError(f"Invalid rank '{rank_ch}' in '{token}': use 1-8.")
    return (row, col)