"""Connect Four - two-player console game."""


from connect_four import COLS, PLAYERS, ConnectFour


def prompt_column(player):
    """Ask the current player for a column until a valid number is given."""
    while True:
        try:
            raw = input(f"Player {player}, choose a column (1-{COLS}): ").strip()
        except EOFError:
            # stdin closed (e.g. Ctrl+D): shut down cleanly, no traceback.
            print("\nInput stream closed - exiting Connect Four.")
            raise SystemExit(0)
        if not raw.isdecimal():
            print("Invalid input: please enter a number.")
            continue
        col = int(raw) - 1
        if not (0 <= col < COLS):
            print(f"Out of range: pick a column between 1 and {COLS}.")
            continue
        return col


def main():
    game = ConnectFour()
    print("Welcome to Connect Four!")
    print("Players alternate turns; first to align four discs wins.")
    game.display()

    while True:
        player = PLAYERS[game.current]
        col = prompt_column(player)
        if not game.is_valid_column(col):
            print("That column is full. Choose another.")
            continue

        row = game.drop_disc(col)
        game.display()

        if game.check_win(row, col):
            print(f"Player {player} wins! Four in a row!")
            break
        if game.is_full():
            print("The grid is full - it's a draw!")
            break

        game.switch_player()


if __name__ == "__main__":
    main()