'''
main.py
Entry point for the Checkers (Draughts) game: renders the board, prompts
each player for moves in from-to notation (e.g. "b3-c4" or "a3-b4-c5"),
validates them against the legal move list, and detects wins/draws.
'''
from game import Game
from position import Position
def parse_move(raw, legal_moves):
    """Parse 'b3-c4' / 'a3-b4-c5' (also accepting 'x' for jumps) into a Move."""
    parts = [p for p in raw.lower().replace("x", "-").split("-") if p]
    if len(parts) < 2:
        raise ValueError("expected at least two squares, e.g. b3-c4")
    path = [Position.from_notation(p) for p in parts]
    for move in legal_moves:
        if move.path == path:
            return move
    raise ValueError("not a legal move for the current player")
def main():
    game = Game()
    print("Checkers — enter moves as from-to notation, e.g. b3-c4 (or a3-b4-c5 for jumps).")
    while True:
        print(game.board)
        moves = game.legal_moves()
        if not moves:
            print(f"{game.current_player.opponent.name_title} wins — no legal moves remain!")
            break
        if game.quiet_plies >= game.QUIET_PLY_LIMIT:
            print("Draw — 40 moves by each side without capture or man advancement.")
            break
        raw = input(f"{game.current_player.name_title} to move: ").strip()
        if raw.lower() in {"q", "quit", "exit"}:
            break
        try:
            move = parse_move(raw, moves)
        except ValueError as exc:
            print(f"Invalid move: {exc}")
            continue
        if game.apply_player_move(move):
            print("Piece crowned!")
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")