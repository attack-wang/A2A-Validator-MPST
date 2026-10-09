from board import BLACK, WHITE

SYMBOLS = {0: '.', 1: 'X', 2: 'O'}


def player_name(player):
    return "X (Black)" if player == BLACK else "O (White)"


def render(board, player, moves):
    move_set = set(moves)
    lines = ["    a b c d e f g h", "  +-----------------+"]
    for r in range(board.size):
        cells = []
        for c in range(board.size):
            if (r, c) in move_set:
                cells.append('*')
            else:
                cells.append(SYMBOLS[board.grid[r][c]])
        lines.append(f"{r + 1} | " + " ".join(cells) + " |")
    lines.append("  +-----------------+")
    black, white = board.score()
    lines.append(f"Score - X (Black): {black}   O (White): {white}")
    if moves:
        coords = " ".join(f"{chr(c + 97)}{r + 1}" for r, c in moves)
        lines.append(f"{player_name(player)} to move. Valid: {coords}")
    else:
        lines.append(f"{player_name(player)} has no valid moves.")
    return "\n".join(lines)


def parse_move(text):
    """Parse input like 'd3' into (row, col); return None if invalid."""
    text = text.strip().lower()
    if len(text) == 2 and text[0].isalpha() and text[1].isdigit():
        c = ord(text[0]) - 97
        r = int(text[1]) - 1
        if 0 <= r < 8 and 0 <= c < 8:
            return r, c
    return None