"""Two-player tic-tac-toe game entry point."""

import sys

from game import Board


def safe_input(prompt):
    """Read input, exiting gracefully if stdin is closed or interrupted."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\nInput closed. Thanks for playing! Goodbye.")
        sys.exit(0)


def get_move(board, player):
    while True:
        try:
            raw = safe_input(f"Player {player}, enter a cell number (1-9): ").strip()
            pos = int(raw) - 1
        except ValueError:
            print("Invalid input. Please enter a number 1-9.")
            continue
        if not 0 <= pos <= 8:
            print("Out of range. Please enter a number 1-9.")
            continue
        if not board.is_empty(pos):
            print("That cell is already taken. Choose another.")
            continue
        return pos


def play_round():
    board = Board()
    current = "X"
    board.display()
    while True:
        pos = get_move(board, current)
        board.place(pos, current)
        board.display()
        winner = board.winner()
        if winner:
            print(f"Player {winner} wins! Congratulations!")
            return winner
        if board.is_full():
            print("It's a draw! The board is full.")
            return None
        current = "O" if current == "X" else "X"


def main():
    print("=== Tic-Tac-Toe ===")
    print("Cells are numbered 1-9, left to right, top to bottom:")
    print(" 1 | 2 | 3 ")
    print("---+---+---")
    print(" 4 | 5 | 6 ")
    print("---+---+---")
    print(" 7 | 8 | 9 ")
    while True:
        play_round()
        again = safe_input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing! Goodbye.")
            break


if __name__ == "__main__":
    main()