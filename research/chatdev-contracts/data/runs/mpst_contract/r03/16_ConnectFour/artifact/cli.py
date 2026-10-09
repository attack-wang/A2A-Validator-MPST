"""Command-line interface and game loop for Connect Four."""

from connect_four import COLS, ConnectFour


def read_column(prompt):
    """Read a column choice; returns a 0-based index, or None if the user quits or input ends."""
    try:
        raw = input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        # Input stream closed or interrupted: end the session gracefully.
        return None
    if raw.lower() in ("q", "quit", "exit"):
        return None
    if not raw.isdigit() or not 1 <= int(raw) <= COLS:
        raise ValueError("enter a number between 1 and {}.".format(COLS))
    return int(raw) - 1


def play():
    """Run a full two-player Connect Four game until win, draw, or quit."""
    game = ConnectFour()
    print("Welcome to Connect Four!")
    print("Type a column number (1-{}) to drop a disc, or 'q' to quit.".format(COLS))
    while True:
        print()
        print(game.display())
        player = game.current_player
        prompt = "\nPlayer {} ({}), choose a column: ".format(player, game.disc(player))
        try:
            col = read_column(prompt)
        except ValueError as exc:
            print("Invalid input: {}".format(exc))
            continue
        if col is None:
            print("Game aborted. Goodbye!")
            return
        if not game.is_valid_column(col):
            print("Column {} is unavailable. Choose another column.".format(col + 1))
            continue
        game.drop_disc(col)
        winner = game.check_win()
        if winner:
            print()
            print(game.display())
            print("\nPlayer {} ({}) wins with four in a row!".format(player, winner))
            return
        if game.is_full():
            print()
            print(game.display())
            print("\nIt's a draw! The grid is full.")
            return
        game.switch_player()


if __name__ == "__main__":
    play()