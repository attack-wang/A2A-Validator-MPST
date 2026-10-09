"""Connect Four: two-player console game. Run with `python main.py`."""

from connect_four import COLS, ConnectFour


def prompt_column(game):
    """Ask the current player for a column until a valid one is given."""
    while True:
        try:
            raw = input(
                f"Player {game.current + 1} ({game.disc}), choose a column 1-{COLS}: "
            )
        except EOFError:
            print("\nInput stream closed — game ended.")
            raise SystemExit(0)
        except KeyboardInterrupt:
            print("\nInterrupted — game ended.")
            raise SystemExit(130)
        raw = raw.strip()
        if not raw.isdigit():
            print("Invalid input: please type a column number.")
            continue
        col = int(raw) - 1
        if not 0 <= col < COLS:
            print(f"Out of range: pick a column between 1 and {COLS}.")
            continue
        if not game.is_valid_column(col):
            print("That column is full. Pick another.")
            continue
        return col


def main():
    game = ConnectFour()
    print("=== Connect Four ===")
    print("Take turns dropping discs; first to connect four wins.")
    game.display()
    while True:
        col = prompt_column(game)
        row = game.drop_disc(col)
        game.display()
        if game.check_win(row, col):
            print(f"Player {game.current + 1} ({game.disc}) connects four — wins!")
            break
        if game.is_full():
            print("The grid is full — it's a draw!")
            break
        game.switch_player()


if __name__ == "__main__":
    main()