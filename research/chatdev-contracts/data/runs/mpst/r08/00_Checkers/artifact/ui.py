'''
ui.py
Console user interface: board rendering, prompts, messages.
'''
from notation import MoveParser
class ConsoleUI:
    """All console input/output for the game, kept out of the game logic."""
    HELP_TEXT = (
        "Move format: <from>-<to>, e.g. 'b2-a3' ('b2xa3' also marks a jump).\n"
        "Squares: column letter a-h + row number 1-8 (row 1 is RED's side).\n"
        "Captures are forced; multi-jumps continue with the same piece.\n"
        "Type 'help' for these instructions, 'quit' to resign."
    )
    @staticmethod
    def show_board(board):
        """Print the current board with blank-line padding."""
        print("\n" + str(board) + "\n")
    @staticmethod
    def show_message(msg):
        """Print an arbitrary message to the user."""
        print(msg)
    @staticmethod
    def show_moves(player, moves):
        """List the player's legal moves in from-to notation."""
        text = ", ".join(
            f"{MoveParser.format_position(m.start)}-{MoveParser.format_position(m.destination)}"
            for m in moves
        )
        ConsoleUI.show_message(f"Legal moves for {player.name}: {text or 'none'}")
    @staticmethod
    def prompt_move(player, forced_piece=None):
        """Prompt until the input is parseable. Returns ((row, col), (row, col)),
        or None if the player chooses to quit/resign."""
        while True:
            if forced_piece is not None:
                prompt = (f"{player.name}, the piece on "
                          f"{MoveParser.format_position(forced_piece)} must keep "
                          f"jumping. Next jump: ")
            else:
                prompt = f"{player.name}, enter your move (e.g. b2-a3): "
            raw = input(prompt).strip()
            if raw.lower() in ("help", "h", "?"):
                print(ConsoleUI.HELP_TEXT)
                continue
            if raw.lower() in ("quit", "q", "exit"):
                return None
            try:
                return MoveParser.parse_move(raw)
            except ValueError as e:
                print(f"Invalid input: {e}")