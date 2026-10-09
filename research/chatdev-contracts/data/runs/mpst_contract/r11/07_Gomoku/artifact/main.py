"""Gomoku - entry point and game loop."""
from board import Board


def parse_move(text, size):
    """Parse 'row col' input; return (r, c) or None if invalid."""
    parts = text.strip().replace(",", " ").split()
    if len(parts) != 2:
        return None
    try:
        r, c = int(parts[0]), int(parts[1])
    except ValueError:
        return None
    if 0 <= r < size and 0 <= c < size:
        return r, c
    return None


def main():
    board = Board()
    players = {1: "Black (X)", 2: "White (O)"}
    current = 1

    print("=== Gomoku (15x15) ===")
    print("Two players alternate: Black (X) and White (O).")
    print("Enter moves as 'row col' using indices 0-14, e.g. '7 7'.")
    print("Type 'q' to quit. First to align 5 stones wins.")
    print(board.render())

    while True:
        name = players[current]
        try:
            raw = input(f"{name}, your move (row col): ")
        except (EOFError, KeyboardInterrupt):
            print("\nGame aborted.")
            return
        raw = raw.strip().lower()
        if raw in ("q", "quit", "exit"):
            print("Game aborted.")
            return

        move = parse_move(raw, board.size)
        if move is None:
            print("Invalid input. Use two integers 0-14, e.g. '7 7'.")
            continue
        r, c = move
        if not board.is_empty(r, c):
            print("Cell occupied. Choose another.")
            continue

        board.place(r, c, current)
        print(board.render())

        if board.check_win(r, c, current):
            print(f"*** {name} wins! ***")
            return
        if board.is_full():
            print("Draw - the board is full.")
            return
        current = 3 - current


if __name__ == "__main__":
    main()