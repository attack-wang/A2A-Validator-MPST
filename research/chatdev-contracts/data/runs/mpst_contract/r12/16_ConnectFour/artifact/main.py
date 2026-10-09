"""Connect Four - command-line two-player game."""

from connect_four import ConnectFour, COLS

SYMBOLS = {0: ".", 1: "X", 2: "O"}


def render(game):
    print()
    for row in game.grid:
        print(" ".join(SYMBOLS[cell] for cell in row))
    print(" ".join(str(c + 1) for c in range(COLS)))


def get_move(game):
    while True:
        try:
            raw = input(
                f"Player {game.current} ({SYMBOLS[game.current]}), "
                f"choose a column (1-{COLS}): "
            )
            col = int(raw) - 1
        except ValueError:
            print("Invalid input: please enter a number.")
            continue
        if not 0 <= col < COLS:
            print(f"Out of range: choose a column between 1 and {COLS}.")
            continue
        if game.is_full(col):
            print("Column is full: choose another column.")
            continue
        return col


def main():
    game = ConnectFour()
    render(game)
    while True:
        col = get_move(game)
        row = game.drop(col)
        render(game)
        if game.check_win(row, col):
            print(f"Player {game.current} ({SYMBOLS[game.current]}) wins!")
            break
        if game.full():
            print("The grid is full. It's a draw!")
            break
        game.switch()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGame aborted.")