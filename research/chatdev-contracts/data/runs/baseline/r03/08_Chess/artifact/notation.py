@staticmethod
def parse(notation, legal_moves, board, color):
    if not notation:
        raise ValueError("empty input")
    text = notation.strip()
    # strip common decorations
    text = text.rstrip('!?#').rstrip('+')  # hmm order
    ...