"""Two-player console tic-tac-toe with a friendly interface."""

from game import Board


def read_cell(board, player):
    """Prompt until the current player picks a valid, free cell."""
    prompt = f"Player {player}, pick a cell (1-9): "
    while True:
        raw = input(prompt).strip()
        if not raw.isdigit():
            print("Please enter a number from 1 to 9.")
            continue
        try:
            board.place(int(raw) - 1, player)
            return
        except ValueError as err:
            print(err)


def play_round():
    board = Board()
    player = "X"
    print("\nNew game! Cells are numbered 1-9, left to right, top to bottom.\n")
    print(board.render())
    while True:
        read_cell(board, player)
        print("\n" + board.render() + "\n")
        winner = board.winner()
        if winner:
            print(f"Player {winner} wins in {len(board.moves)} moves!")
            print("Move history:", board.moves)
            return
        if board.is_full():
            print("It's a draw!")
            print("Move history:", board.moves)
            return
        player = "O" if player == "X" else "X"


def main():
    print("=== Tic-Tac-Toe ===")
    while True:
        play_round()
        if input("\nPlay again? (y/n): ").strip().lower() != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()