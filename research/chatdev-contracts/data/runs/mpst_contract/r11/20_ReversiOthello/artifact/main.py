"""Reversi (Othello) console game — entry point and game loop."""

from game import ReversiGame, BLACK, WHITE
import ui


def safe_input(prompt):
    """Read a line of input, exiting cleanly if stdin is closed or interrupted."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\nInput stream closed — exiting.")
        raise SystemExit(0)


def choose_mode():
    print("=== Reversi (Othello) ===")
    print("1) Human vs Human")
    print("2) Human vs Computer (computer plays White)")
    while True:
        choice = safe_input("Select mode [1/2]: ").strip()
        if choice in ("1", "2"):
            return int(choice)
        print("Please enter 1 or 2.")


def computer_move(game):
    """Greedy AI: choose the valid move that flips the most discs."""
    moves = game.valid_moves()
    return max(moves, key=lambda m: len(moves[m]))


def play():
    mode = choose_mode()
    game = ReversiGame()
    print("Enter moves as 'row col' (e.g. '3 4'). '*' marks valid moves. 'q' quits.")
    while not game.game_over():
        if not game.has_valid_move(game.current):
            name = "Black" if game.current == BLACK else "White"
            print(f"{name} has no valid move — turn passes.")
            game.switch_player()
            continue
        print()
        print(ui.render(game))
        name = "Black" if game.current == BLACK else "White"
        if mode == 2 and game.current == WHITE:
            r, c = computer_move(game)
            print(f"Computer ({name}) plays: {r + 1} {c + 1}")
            game.apply_move(r, c)
            game.switch_player()
            continue
        text = safe_input(f"{name} ({game.current}) move: ").strip()
        if text.lower() in ("q", "quit"):
            print("Game aborted.")
            return
        move = ui.parse_move(text)
        if move is None or not game.is_valid_move(*move):
            print("Invalid move. Try again.")
            continue
        game.apply_move(*move)
        game.switch_player()
    ui.announce_result(game)


if __name__ == "__main__":
    play()