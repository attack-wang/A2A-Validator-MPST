"""Console rendering and input parsing for Reversi."""

from game import BLACK, WHITE, EMPTY, SIZE


def render(game, show_moves=True):
    """Return the board as text; '*' marks valid moves for the current player."""
    moves = game.valid_moves() if show_moves else {}
    lines = ["   " + " ".join(str(c + 1) for c in range(SIZE))]
    for r in range(SIZE):
        row = []
        for c in range(SIZE):
            cell = game.board[r][c]
            row.append("*" if cell == EMPTY and (r, c) in moves else cell)
        lines.append(f" {r + 1} " + " ".join(row))
    b, w = game.score()
    lines.append(f"Score -> Black (B): {b}  White (W): {w}")
    return "\n".join(lines)


def parse_move(text):
    """Parse 'row col' input like '3 4' or '3,4' into 0-based (r, c), or None."""
    parts = text.replace(",", " ").split()
    if len(parts) != 2:
        return None
    try:
        r, c = int(parts[0]) - 1, int(parts[1]) - 1
    except ValueError:
        return None
    if 0 <= r < SIZE and 0 <= c < SIZE:
        return r, c
    return None


def announce_result(game):
    print(render(game, show_moves=False))
    b, w = game.score()
    if b > w:
        print(f"Game over! Black wins {b}-{w}.")
    elif w > b:
        print(f"Game over! White wins {w}-{b}.")
    else:
        print(f"Game over! It's a tie {b}-{w}.")