"""Connect Four - two-player console game."""
from connect_four import COLS, ConnectFour


def read_column(game):
    """Prompt until the current player enters a valid, non-full column."""
    while True:
        raw = input(f"Player {game.current}, choose a column (1-{COLS}): ").strip()
        if not raw.isdigit():
            print("Invalid input: please type a number.")
            continue
        col = int(raw) - 1
        if not game.is_valid_column(col):
            print("Invalid column: out of range or already full. Try again.")
            continue
        return col


def main():
    game = ConnectFour()
    print("=== Connect Four ===")
    print("Players X and O alternate turns; type a column number to drop a disc.")
    print("First to line up four discs horizontally, vertically, or diagonally wins.")
    game.display()
    while True:
        col = read_column(game)
        row = game.drop_disc(col)
        game.display()
        if game.check_win(row, col):
            print(f"Player {game.current} wins! Four discs in a line.")
            break
        if game.is_full():
            print("It's a draw! The grid is full.")
            break
        game.switch_player()


if __name__ == "__main__":
    main()