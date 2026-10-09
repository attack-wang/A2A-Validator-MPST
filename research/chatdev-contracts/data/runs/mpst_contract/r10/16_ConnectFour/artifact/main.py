"""Connect Four - two-player console game entry point."""

from connect_four import Board, COLS


def get_move(board, player):
    """Prompt until the player enters a valid, non-full column number."""
    while True:
        raw = input(f"Player {player}, choose a column (1-{COLS}): ").strip()
        if not raw.isdigit():
            print("Invalid input: please enter a number.")
            continue
        col = int(raw) - 1
        if not (0 <= col < COLS):
            print(f"Column out of range. Choose 1-{COLS}.")
            continue
        if not board.is_valid_column(col):
            print("That column is full. Choose another.")
            continue
        return col


def main():
    board = Board()
    players = ["X", "O"]
    turn = 0
    print("Welcome to Connect Four! Connect four discs in a row to win.")
    board.display()
    while True:
        player = players[turn % 2]
        col = get_move(board, player)
        board.drop_disc(col, player)
        board.display()
        if board.check_win(player):
            print(f"Player {player} wins! Four in a row!")
            break
        if board.is_full():
            print("It's a draw! The grid is full.")
            break
        turn += 1


if __name__ == "__main__":
    main()