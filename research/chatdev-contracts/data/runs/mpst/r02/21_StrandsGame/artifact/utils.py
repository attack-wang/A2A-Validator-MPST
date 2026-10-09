def normalize(text):
    """Uppercase and strip non-letter chars so strand/target comparisons are consistent."""
    return "".join(ch for ch in text.upper() if ch.isalpha())
def parse_selection(raw, max_index):
    """Parse a comma-separated selection string into a list of 1-based ints.
    Returns (ok, indices_or_error_message)."""