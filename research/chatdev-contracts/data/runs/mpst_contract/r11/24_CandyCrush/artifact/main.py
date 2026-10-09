import sys
from game import Board

DIRS = {"u": (-1, 0), "d": (1, 0), "l": (0, -1), "r": (0, 1)}
TARGET = 500
MAX_MOVES = 20


def render(board):
    print("\n    " + " ".join(str(c) for c in range(board.cols)))
    for r in range(board.rows):
        print(f"  {r} " + " ".join(board.grid[r]))
    print(f"\n  Score: {board.score}/{TARGET}   Moves left: {MAX_MOVES - board.moves}")


def read_line(text):
    try:
        return input(text)
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def prompt(board):
    raw = read_line("\nMove (row col u/d/l/r, 'n' new, 'q' quit): ")
    if raw is None:
        return "quit"
    raw = raw.strip().lower()
    if raw in ("q", "quit", "exit"):
        return "quit"
    if raw in ("n", "new"):
        return "new"
    parts = raw.replace(",", " ").split()
    if len(parts) != 3 or parts[2] not in DIRS:
        print("  Invalid input.")
        return None
    try:
        r, c = int(parts[0]), int(parts[1])
    except ValueError:
        print("  Invalid input.")
        return None
    dr, dc = DIRS[parts[2]]
    result = board.move(r, c, r + dr, c + dc)
    if result is None:
        print("  Invalid move (no match formed).")
        return None
    gained, chain = result
    msg = f"  +{gained} points"
    if chain > 1:
        msg += f"  (chain x{chain}!)"
    print(msg)
    return None


def main():
    print("=" * 40)
    print("  CANDY MATCH - a match-3 puzzle")
    print("=" * 40)
    print("Swap adjacent candies to line up 3 or more.")
    print(f"Reach {TARGET} points within {MAX_MOVES} moves.")
    board = Board()
    while True:
        render(board)
        if board.score >= TARGET:
            print("\n  *** YOU WIN! ***")
            break
        if board.moves >= MAX_MOVES:
            print("\n  Out of moves. YOU LOSE.")
            break
        action = prompt(board)
        if action == "quit":
            print(f"\n  Final score: {board.score}. Bye!")
            break
        if action == "new":
            board = Board()
            print("  New game started.")
    return 0


if __name__ == "__main__":
    sys.exit(main())