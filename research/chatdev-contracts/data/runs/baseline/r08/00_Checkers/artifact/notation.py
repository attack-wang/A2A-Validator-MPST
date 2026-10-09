import re
def parse_move(text):
    """
    Parses move notation. Supported formats:
      - 'b2-c3', 'b2 c3', 'b2 to c3', 'b2xc3'
      - '3,2-4,3' (row,col numeric, 1-indexed display rows)
    Returns ((from_row, from_col), (to_row, to_col)) in 0-indexed internal coords,
    or raises ValueError with a helpful message.
    """
    if not text or not text.strip():
        raise ValueError("Empty input. Enter a move like 'b2-c3' or type 'help'.")
    s = text.strip().lower()
    # Algebraic format: e.g. b2-c3, b2xc3, b2 to c3, b2 c3
    m = re.match(r'^([a-h])([1-8])\s*(?:[-xX]|to|\s)\s*([a-h])([1-8])$', s)
    if m:
        from_col = ord(m.group(1)) - ord('a')
        from_row = 8 - int(m.group(2))
        to_col = ord(m.group(3)) - ord('a')
        to_row = 8 - int(m.group(4))
        return ((from_row, from_col), (to_row, to_col))
    # Numeric format: e.g. 3,2-4,3 (display rows 1-indexed top-down)
    m = re.match(r'^([1-8])\s*,\s*([1-8])\s*(?:[-xX]|to|\s)\s*([1-8])\s*,\s*([1-8])$', s)
    if m:
        from_row = 8 - int(m.group(1))
        from_col = int(m.group(2)) - 1
        to_row = 8 - int(m.group(3))
        to_col = int(m.group(4)) - 1
        return ((from_row, from_col), (to_row, to_col))
    raise ValueError(
        "Could not parse move. Use notation like 'b2-c3' (or 'b2xc3' for a jump), "
        "or numeric '3,2-4,3'. Type 'help' for details."
    )