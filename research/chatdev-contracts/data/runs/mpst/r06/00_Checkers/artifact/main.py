'''
main.py
Entry point: runs the interactive two-player checkers game loop.
'''
from pieces import PieceColor
from game import Game
from move_parser import parse_move
COLOR_NAMES = {PieceColor.RED: "Red", PieceColor.BLACK: "Black"}
def print_help():
    '''Print a short explanation of the input notation and commands.'''
    print(
        """
Commands:
  <move>   Play a move, e.g. 'c3-d4', 'c3 d4', 'c3 to d4', 'c3xe5',
           or a full jump chain like 'c3-e5-g7'. For a jump with a
           unique landing square you may give just 'from-to'.
  board    Show the board again.
  help     Show this help text.
  quit     Resign and exit.
Notation: columns are letters a-h (left to right), rows are 1-8
(bottom to top). Red moves first and moves up the board; Black
moves down. Captures are compulsory. Kings are shown as R/B.
"""
    )
def describe_legal_moves(game):
    '''Return a human-readable list of the current player's legal moves.'''
    moves = game.legal_moves()
    if not moves:
        return "none"
    return ", ".join(repr(m).replace("Move(", "").rstrip(")") for m in moves)
def main():
    game = Game()
    print("=== Checkers (Draughts) ===")
    print("Two-player console game. Type 'help' for the notation, 'quit' to exit.")
    while not game.game_over:
        game.board.display()
        color = game.current_color
        moves = game.legal_moves()
        must_capture = bool(moves) and moves[0].is_capture
        hint = "captures are compulsory" if must_capture else "no capture available"
        print(f"Legal moves for {COLOR_NAMES[color]}: {describe_legal_moves(game)}")
        try:
            text = input(f"{COLOR_NAMES[color]} to move ({hint}): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGame aborted.")
            return
        if not text:
            continue
        command = text.lower()
        if command in ("quit", "exit", "resign"):
            print(f"{COLOR_NAMES[color]} resigns. Game aborted.")
            return
        if command == "help":
            print_help()
            continue
        if command == "board":
            continue
        try:
            waypoints = parse_move(text)
        except ValueError as exc:
            print(f"Invalid input: {exc}")
            continue
        move = game.find_matching_move(waypoints)
        if move is None:
            print("Illegal move. Check the list of legal moves above and try again.")
            continue
        game.apply_move(move)
        if move.is_capture:
            print(f"Captured {len(move.captures)} piece(s).")
    game.board.display()
    if game.winner is not None:
        print(f"Game over — {COLOR_NAMES[game.winner]} wins!")
    else:
        print("Game over.")
if __name__ == "__main__":
    main()