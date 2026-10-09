@staticmethod
def parse_move(text):
    tokens = re.split(r'[-\s,]+', text.strip().lower())
    path = []
    for tok in tokens:
        m = re.fullmatch(r'([a-h])([1-8])', tok)
        if not m:
            return None
        col = ord(m.group(1)) - ord('a')
        row = 8 - int(m.group(2))
        path.append((row, col))
    if len(path) < 2:
        return None
    return path