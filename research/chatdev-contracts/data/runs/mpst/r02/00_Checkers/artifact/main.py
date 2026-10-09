'''
Entry point and interactive console loop for the Checkers (Draughts) game.
Run with:  python main.py
Moves are entered in algebraic notation: "b6-d8" for a simple move or
"b6-d8-f6" for a chained double jump ("-" or spaces may separate squares).
Type "help" for the command list, "moves" for legal moves, "board" to
redraw the board and "quit" to exit.
'''
import sys
from constants import RED
from game import CheckersGame, IllegalMoveError, square_name
class MoveParseError(ValueError):
    """Raised when move text cannot be parsed into board squares."""
FILES = "abcdefgh"
def _square_to_pos(token):
    """Convert a square name such as 'b6' into internal (row, col)."""
    token = token.strip().lower()
    if len(token) != 2 or token[0] not in FILES or not token[1].isdigit():
        raise MoveParseError(f"'{token}' is not a square such as 'b6'.")
    col = FILES.index(token[0])
    rank = int(token[1])
    if not 1 <= rank <= 8:
        raise MoveParseError(f"Rank '{token[1]}' is out of range (use 1-8).")
    row = 8 - rank
    if (row + col) % 2 == 0:
        raise MoveParseError(
            f"'{token}' is a light square; pieces only stand on dark squares.")
    return (row, col)
def parse_move(text):
    """Parse 'b6-d8' or 'b6 d8' or 'b6-d8-f6' into list of (row, col). Raises MoveParseError."""
    text = text.strip().lower().replace(" ", "-")
    tokens = [t for t in text.split("-") if t]
    if len(tokens) < 2:
        raise MoveParseError(
            "A move needs a 'from' and a 'to' square, e.g. b6-d8.")
    return [_square_to_pos(t) for t in tokens]
HELP_TEXT = """\
Commands:
  b6-d8        move/capture from b6 to d8 ('-' or spaces separate squares)
  b6-d8-f6     chained multi-jump
  moves        list all legal moves for the player on turn
  board        redraw the board
  help         show this help
  quit         leave the game
Rules:
  * Red moves first; the two players alternate turns.
  * Men move one square diagonally forward; kings move diagonally both ways.
  * Captures are compulsory jumps over an adjacent enemy piece.
  * Multi-jumps must be completed: after a jump you keep jumping with the
    same piece while further jumps are available.
  * A man reaching the far rank is crowned a king (upper-case symbol);
    the move then ends.
  * A player loses when left with no pieces or no legal move.
"""
def show_moves(game):
    """Print every legal move of the player on turn."""
    moves = game.get_all_moves(game.current_player)
    if not moves:
        print("  No legal moves left.")
        return
    names = sorted({"-".join(square_name(p) for p in path) for path in moves})
    print("  Legal moves: " + ", ".join(names))
def report_move(path, result):
    """Print a short summary of an applied move."""
    parts = []
    if result["captured"]:
        names = ", ".join(square_name(p) for p in result["captured"])
        parts.append(f"captured {len(result['captured'])} piece(s) on {names}")
    if result["crowned"]:
        parts.append(f"the piece on {square_name(path[-1])} was crowned")
    if result["continue_from"] is not None:
        parts.append(f"keep jumping with the piece on "
                     f"{square_name(result['continue_from'])}")
    if parts:
        print("  " + "; ".join(parts) + ".")
    else:
        print("  Move played.")
def main():
    game = CheckersGame(starting_player=RED)
    print("=== Checkers (Draughts) ===")
    print("Red (r/R) moves first and plays up the board; "
          "Black (b/B) plays down. Kings are upper-case.")
    print("Type 'help' for commands.")
    while True:
        print()
        print(game.board.display())
        player = game.current_player
        if game.continuation_from is not None:
            prompt = (f"{player} must continue jumping with the piece on "
                      f"{square_name(game.continuation_from)}: ")
        else:
            prompt = f"{player}'s move (e.g. b6-d8): "
        try:
            text = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGame aborted.")
            return
        if not text:
            continue
        command = text.lower()
        if command in ("quit", "exit"):
            print("Thanks for playing!")
            return
        if command == "help":
            print(HELP_TEXT)
            continue
        if command == "board":
            continue
        if command == "moves":
            show_moves(game)
            continue
        try:
            path = parse_move(text)
            result = game.apply_move(path)
        except (MoveParseError, IllegalMoveError) as exc:
            print(f"  ! {exc}")
            continue
        report_move(path, result)
        if game.is_game_over():
            print()
            print(game.board.display())
            winner = game.get_winner()
            print(f"Game over - {winner} wins!")
            return
if __name__ == "__main__":
    main()