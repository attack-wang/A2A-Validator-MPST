"""Tic-Tac-Toe: two-player console game entry point."""

from game import TicTacToe


def safe_input(prompt):
    """Read a line of input, treating EOF/interrupt as a quit signal.

    Returns the entered string, or None if the input stream is closed
    (e.g. non-interactive stdin) or the user presses Ctrl+C/D.
    """
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def prompt_move(game):
    """Ask the current player for a move until a valid one is entered.

    Returns the board index, or None if the player quits.
    """
    while True:
        raw = safe_input(
            f"Player {game.current_player}, enter your move as row,col (1-3): "
        )
        if raw is None:
            return None
        raw = raw.strip()
        if raw.lower() in ("q", "quit", "exit"):
            return None
        index = game.position_to_index(raw)
        if index is None:
            print("Invalid input. Use row,col with numbers 1-3 (e.g. 2,3).")
        elif not game.is_valid_move(index):
            print("That cell is already taken. Choose an empty cell.")
        else:
            return index


def print_header():
    print("=" * 32)
    print("          TIC-TAC-TOE")
    print("=" * 32)
    print("Two players alternate placing X and O.")
    print("Enter moves as 'row,col' using numbers 1-3.")
    print("Type 'q' at any prompt to quit.")
    TicTacToe.display_guide()


def play_round():
    """Play one full game until a player wins or the board is full.

    Returns True if the round finished (win/draw), False if aborted.
    """
    game = TicTacToe()
    print_header()
    game.display()

    while True:
        index = prompt_move(game)
        if index is None:
            print("Game aborted. Thanks for playing!")
            return False
        game.make_move(index)
        game.display()

        winner = game.check_winner()
        if winner:
            print(f"*** Player {winner} wins! ***")
            break
        if game.is_full():
            print("*** It's a draw! The board is full. ***")
            break
        game.switch_player()

    history = game.move_history()
    print("Move history:", " ".join(history) if history else "none")
    return True


def main():
    while True:
        play_round()
        again = safe_input("Play again? (y/n): ")
        if again is None or again.strip().lower() not in ("y", "yes"):
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()