"""Reversi (Othello) console game entry point."""

from game import ReversiGame


def render(game):
    print("\n   " + " ".join(str(c + 1) for c in range(8)))
    for r in range(8):
        print(f"{r + 1}  " + " ".join(game.board[r]))
    b, w = game.score()
    print(f"\nScore - Black (B): {b}  White (W): {w}")
    if not game.is_over():
        print(f"Turn: {game.current}")


def parse_move(text):
    parts = text.strip().split()
    if len(parts) != 2:
        return None
    try:
        r, c = int(parts[0]) - 1, int(parts[1]) - 1
    except ValueError:
        return None
    if 0 <= r < 8 and 0 <= c < 8:
        return r, c
    return None


def read_move(prompt):
    """Read a move, returning None on EOF/interrupt instead of crashing."""
    try:
        return input(prompt).strip().lower()
    except (EOFError, KeyboardInterrupt):
        return None


def main():
    game = ReversiGame()
    print("=== Reversi (Othello) ===")
    print("Enter moves as 'row col' (1-8), e.g. '4 3'. Type 'q' to quit.")
    while not game.is_over():
        render(game)
        moves = game.valid_moves()
        if not moves:
            print(f"No valid moves for {game.current}. Passing...")
            game.advance_turn()
            continue
        legal = " ".join(f"{r + 1},{c + 1}" for r, c in sorted(moves))
        print(f"Valid moves: {legal}")
        text = read_move(f"{game.current} move: ")
        if text is None:
            print("\nInput stream closed. Game aborted.")
            return
        if text in ("q", "quit"):
            print("Game aborted.")
            return
        pos = parse_move(text)
        if pos is None or pos not in moves:
            print("Invalid move, try again.")
            continue
        game.apply_move(*pos)
    render(game)
    b, w = game.score()
    if b > w:
        winner = "Black wins!"
    elif w > b:
        winner = "White wins!"
    else:
        winner = "It's a tie!"
    print(f"\nGame over. Final score - Black: {b}, White: {w}. {winner}")


if __name__ == "__main__":
    main()