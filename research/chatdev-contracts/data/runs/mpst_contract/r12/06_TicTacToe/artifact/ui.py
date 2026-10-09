"""Console interface helpers for the tic-tac-toe game."""


def read_line(prompt):
    """Read a line of input. Returns None if stdin is closed or interrupted."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def print_board(board):
    """Display the 3x3 grid, showing cell numbers for empty cells."""
    print()
    for row in range(3):
        cells = []
        for col in range(3):
            value = board[row * 3 + col]
            cells.append(value if value != " " else str(row * 3 + col + 1))
        print("  {} | {} | {}".format(*cells))
        if row < 2:
            print(" ---+---+---")
    print()


def prompt_move(player, valid):
    """Ask the current player for a move. Returns a valid position, or None to quit."""
    while True:
        raw = read_line("Player {} - enter a position (1-9) or 'q' to quit: ".format(player))
        if raw is None:
            return None
        raw = raw.strip()
        if raw.lower() == "q":
            return None
        if raw.isdigit() and int(raw) in valid:
            return int(raw)
        print("Invalid move. Empty cells: {}".format(", ".join(map(str, valid))))


def announce(result):
    """Report the final outcome of the round."""
    if result == "Draw":
        print("It's a draw! The board is full.")
    else:
        print("Player {} wins! Three in a row.".format(result))


def play_again():
    """Ask whether the players want another round."""
    raw = read_line("Play again? (y/n): ")
    return raw is not None and raw.strip().lower() == "y"