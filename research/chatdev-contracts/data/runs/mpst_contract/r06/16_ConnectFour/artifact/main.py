from connect_four import ConnectFour, COLS


def read_choice(prompt):
    """Read a line from stdin; treat EOF or interrupt as a quit request."""
    try:
        return input(prompt).strip().lower()
    except EOFError:
        print()
        return 'q'
    except KeyboardInterrupt:
        print()
        return 'q'


def main():
    game = ConnectFour()
    print("Connect Four - Players X and O alternate; type a column number 1-7 (or 'q' to quit).")
    while True:
        game.display()
        choice = read_choice(f"Player {game.current}, choose a column (1-{COLS}): ")
        if choice in ('q', 'quit', 'exit'):
            print("Game ended by player. Goodbye!")
            break
        if not choice.isdigit() or not 1 <= int(choice) <= COLS:
            print(f"Invalid input: enter a number between 1 and {COLS}.")
            continue
        col = int(choice) - 1
        row = game.drop(col)
        if row is None:
            print("That column is full. Choose another.")
            continue
        if game.is_win(row, col):
            game.display()
            print(f"Player {game.current} wins! Four in a row!")
            break
        if game.is_full():
            game.display()
            print("The grid is full - it's a draw!")
            break
        game.switch()


if __name__ == '__main__':
    main()