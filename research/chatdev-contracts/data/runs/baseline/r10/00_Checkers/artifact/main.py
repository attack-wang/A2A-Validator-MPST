'''
main.py
Entry point of the Checkers (Draughts) game. Runs the interactive loop:
renders the board, prompts the side to move for algebraic notation
(e.g. 'b6-a5'), validates the move against the rules and applies it.
Special commands: 'l' lists legal moves, 'h' shows help, 'q' quits.
'''
from piece import PieceColor
from game import Game
HELP_TEXT = ("Enter a move in notation like b6-a5 (from-to). "
             "Commands: l = list legal moves, h = help, q = quit.")
def main():
    """Run the interactive two-player checkers loop."""
    game = Game()
    print("Welcome to Checkers (Draughts)!")
    print("Black (b) moves first. Kings are shown in uppercase (B/R).")
    print(HELP_TEXT)
    while True:
        game.board.display()
        red_count = game.board.count_pieces(PieceColor.RED)
        black_count = game.board.count_pieces(PieceColor.BLACK)
        print(f"Pieces - Red: {red_count}, Black: {black_count}")
        winner = game.check_winner()
        if winner is not None:
            print(f"Game over - {winner.name_str} wins!")
            break
        if game.mid_jump is not None:
            prompt = (f"{game.turn.name_str}'s turn - capture! You must keep "
                      f"jumping with {to_notation(*game.mid_jump)}: ")
        else:
            prompt = f"{game.turn.name_str}'s turn. Enter move (e.g. b6-a5): "
        try:
            raw = input(prompt).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nGame aborted. Thanks for playing!")
            break
        if raw == "q":
            print("Thanks for playing!")
            break
        if raw == "h":
            print(HELP_TEXT)
            continue
        if raw == "l":
            moves = game.get_legal_moves()
            listing = ", ".join(format_move(m) for m in moves) or "none"
            print(f"Legal moves: {listing}")
            continue
        try:
            src, dst = game.parse_move(raw)
        except ValueError as error:
            print(f"Invalid input: {error}")
            continue
        if (src, dst) not in game.get_legal_moves():
            print("That move is not legal (remember: captures are forced). "
                  "Type 'l' to list legal moves.")
            continue
        if game.apply_move(src, dst):
            print("Capture! Continue jumping with the same piece.")
if __name__ == "__main__":
    main()