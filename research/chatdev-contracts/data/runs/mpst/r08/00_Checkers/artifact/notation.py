'''
notation.py
Parsing of user move input in algebraic-like checkers notation.
'''
class MoveParser:
    """Converts text like 'b2-a3' into internal (row, col) positions."""
    COLS = "abcdefgh"
    @classmethod
    def parse_position(cls, text):
        """Parse a single square such as 'b2' into (row, col); row 1 is RED's side."""
        text = text.strip().lower()
        if len(text) != 2:
            raise ValueError(
                f"Invalid position '{text}'. Use column letter a-h + row number 1-8, e.g. 'b2'.")
        col_char, row_char = text[0], text[1]
        if col_char not in cls.COLS:
            raise ValueError(
                f"Invalid column '{col_char}' in '{text}'. Column must be a-h.")
        if not row_char.isdigit() or not (1 <= int(row_char) <= 8):
            raise ValueError(
                f"Invalid row '{row_char}' in '{text}'. Row must be 1-8.")
        col = cls.COLS.index(col_char)
        row = int(row_char) - 1
        return (row, col)
    @classmethod
    def parse_move(cls, text):
        """Parse 'b2-a3', 'b2xa3', 'b2 a3', 'b2:a3' or 'b2 to a3' into two
        (row, col) positions; raises ValueError on malformed input."""
        normalized = text.strip().lower().replace(" to ", "-")
        for sep in ("-", "x", ":", " "):
            if sep in normalized:
                parts = [p for p in normalized.split(sep) if p]
                break
        else:
            raise ValueError(
                f"Invalid move '{text}'. Use from-to notation, e.g. 'b2-a3'.")
        if len(parts) != 2:
            raise ValueError(
                f"Invalid move '{text}'. Enter exactly two squares, e.g. 'b2-a3'.")
        return cls.parse_position(parts[0]), cls.parse_position(parts[1])
    @classmethod
    def format_position(cls, pos):
        """Convert an internal (row, col) back to 'b2'-style text for display."""
        row, col = pos
        return f"{cls.COLS[col]}{row + 1}"