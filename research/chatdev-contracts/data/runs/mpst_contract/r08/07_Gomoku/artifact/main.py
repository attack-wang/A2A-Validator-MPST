"""Entry point for the console Gomoku game (15x15, two players)."""

from game import Board, BLACK, WHITE, EMPTY


def parse_move(text):
    """Parse 'row col' input; return (row, col) or None if invalid."""
    parts = text.strip().split()
    if len(parts) != 2:
        return None
    try:
        row, col = int(parts[0]), int(parts[1])
    except ValueError:
        return None
    return row, col


def read_move(prompt):
    """Read a line from stdin; return None on EOF or interrupt."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def main():
    board = Board()
    players = {BLACK: "Black (X)", WHITE: "White (O)"}
    current = BLACK

    print("Welcome to Gomoku (15x15 board).")
    print("Enter moves as: row col (e.g., '7 7'). Rows and columns are 0-14.")
    print("Five in a row (horizontal, vertical, or diagonal) wins. Type 'quit' to exit.\n")

    while True:
        print(board.render())
        print(f"\n{players[current]}'s turn.")
        raw = read_move("Move: ")
        if raw is None:
            print("Input stream closed. Game aborted. Goodbye!")
            return

        text = raw.strip().lower()
        if text in ("quit", "exit", "q"):
            print("Game aborted. Goodbye!")
            return

        move = parse_move(text)
        if move is None:
            print("Invalid input. Enter two integers separated by a space: row col.\n")
            continue

        row, col = move
        if not board.place(row, col, current):
            print("Invalid move: out of bounds or occupied cell.\n")
            continue

        winner = board.check_win(row, col)
        if winner != EMPTY:
            print(board.render())
            print(f"\n{players[winner]} wins with five in a row!")
            return

        if board.is_full():
            print(board.render())
            print("\nThe board is full. It's a draw!")
            return

        current = WHITE if current == BLACK else BLACK


if __name__ == "__main__":
    main()