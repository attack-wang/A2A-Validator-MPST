def parse_square(text):
    """
    Convert user input like 'b3' (or '3b') into (row, col) grid coordinates.
    Returns None if the text is not a valid square.
    """
    text = text.strip().lower()
    if len(text) == 2:
        if text[0].isalpha() and text[1].isdigit():
            file_ch, rank_ch = text[0], text[1]
        elif text[0].isdigit() and text[1].isalpha():
            file_ch, rank_ch = text[1], text[0]
        else:
            return None
    else:
        return None
    col = ord(file_ch) - ord('a')
    rank = int(rank_ch)
    if not (0 <= col < Board.SIZE and 1 <= rank <= Board.SIZE):
        return None
    row = Board.SIZE - rank
    return (row, col)