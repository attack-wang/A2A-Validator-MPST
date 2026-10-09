"""Tic-tac-toe: two-player console game with a user-friendly interface."""

from game import Board


def safe_input(prompt):
    """Read a line; exit gracefully if the input stream closes (EOF/Ctrl-C)."""
    try:
        return input(prompt)
    except EOFError:
        print("\nInput stream closed. Goodbye.")
        raise SystemExit(0)
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye.")
        raise SystemExit(0)


def read_move(board, player):
    """Prompt until the current player enters a valid empty cell (1-9)."""
    while True:
        raw = safe_input(f"Player {player}, choose a cell 1-9: ").strip()
        if not raw.isdigit():
            print("Please enter a number from 1 to 9.")
            continue
        pos = int(raw) - 1
        if not 0 <= pos <= 8:
            print("That number is out of range. Try 1-9.")
        elif not board.is_free(pos):
            print("That cell is already taken. Pick another.")
        else:
            return pos


def play_round():
    """Run one full game; return 'X', 'O', or None for a draw."""
    board = Board()
    current = "X"
    print("\nNew game! X goes first.")
    print("Cells are numbered 1-9 like this:")
    print(board.render())
    while True:
        pos = read_move(board, current)
        board.place(pos, current)
        print("\n" + board.render())
        win = board.winner()
        if win:
            print(f"\nPlayer {win} wins! Congratulations!")
            print("Move history: " + ", ".join(f"{m}->{p}" for m, p in board.history))
            return win
        if board.is_full():
            print("\nIt's a draw! The board is full.")
            print("Move history: " + ", ".join(f"{m}->{p}" for m, p in board.history))
            return None
        current = "O" if current == "X" else "X"


def main():
    print("=" * 30)
    print("      TIC-TAC-TOE (2 PLAYERS)")
    print("=" * 30)
    scores = {"X": 0, "O": 0, "draws": 0}
    while True:
        result = play_round()
        if result:
            scores[result] += 1
        else:
            scores["draws"] += 1
        print(f"Score -> X: {scores['X']}  O: {scores['O']}  Draws: {scores['draws']}")
        again = safe_input("Play again? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("Thanks for playing! Goodbye.")
            break


if __name__ == "__main__":
    main()