"""Two-player tic-tac-toe with a friendly command-line interface."""

from game import Board


def read_line(prompt):
    """Read one line of input, exiting gracefully if stdin is closed."""
    try:
        return input(prompt)
    except EOFError:
        print("\nInput stream closed. Thanks for playing! Goodbye.")
        raise SystemExit(0)


def get_move(board, player):
    """Prompt the current player until a valid, open cell number is given."""
    prompt = f"Player {player}, choose a cell (1-9): "
    while True:
        choice = read_line(prompt).strip()
        if board.is_valid_move(choice):
            return int(choice)
        if choice.isdigit() and 1 <= int(choice) <= 9:
            print("That cell is already taken. Try again.")
        else:
            print("Please enter a number from 1 to 9.")


def play_round():
    """Run one full game until a player wins or the board is full."""
    board = Board()
    player = "X"
    while True:
        print("\n" + board.display())
        board.make_move(get_move(board, player), player)
        winner = board.check_winner()
        if winner:
            print("\n" + board.display())
            print(f"Player {winner} wins! Congratulations!")
            return
        if board.is_full():
            print("\n" + board.display())
            print("It's a draw! The board is full.")
            return
        player = "O" if player == "X" else "X"


def main():
    print("Welcome to Tic-Tac-Toe!")
    print("Player 1 is X, Player 2 is O. Pick a cell by its number (1-9).")
    while True:
        play_round()
        if read_line("\nPlay again? (y/n): ").strip().lower() != "y":
            print("Thanks for playing! Goodbye.")
            break


if __name__ == "__main__":
    main()