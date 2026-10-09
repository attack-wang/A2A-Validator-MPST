'''
ui.py
Terminal front-end for Strands.
TerminalUI handles everything the player sees and types:
  * rendering the board (with found-word highlighting and hint reveals)
  * parsing coordinate input in two formats:
        "0,0 1,1 2,2"   (row,col pairs)
        "A1 B2 C3"      (column letter + 1-based row)
  * printing feedback, progress and help text
'''
import string
class TerminalUI:
    """Renders the board and messages; parses player input."""
    COLORS = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "dim": "\033[2m",
        "cyan": "\033[96m",
        "yellow": "\033[93m",
        "green": "\033[92m",
        "magenta": "\033[95m",
        "red": "\033[91m",
    }
    COMMANDS = ("hint", "help", "quit", "found")
    def __init__(self, use_color=True):
        self.use_color = use_color
    def _c(self, name, text):
        if not self.use_color:
            return text
        return self.COLORS.get(name, "") + text + self.COLORS["reset"]
    def show_welcome(self, puzzle):
        print("=" * 60)
        print(self._c("bold", "  S T R A N D S"))
        print(f"  Puzzle: {puzzle.name}")
        print(f"  Theme : {puzzle.theme}")
        print("=" * 60)
        print("Trace adjacent letters to merge theme words.")
        print("Type 'help' for instructions.")
    def show_board(self, puzzle, game):
        claimed = game.claimed_cells()
        revealed = game.revealed_cells
        col_letters = string.ascii_uppercase[:puzzle.cols]
        header = "    " + "  ".join(col_letters)
        print(header)
        for r in range(puzzle.rows):
            row_cells = []
            for c in range(puzzle.cols):
                ch = puzzle.letter_at(r, c)
                if (r, c) in claimed:
                    cell = self._c("cyan", ch)      # color only: width stays 1
                elif (r, c) in revealed:
                    cell = self._c("yellow", ch)    # FIX: no '*' suffix
                else:
                    cell = ch
                row_cells.append(cell)
            print(f"  {r} " + "  ".join(row_cells))
        print()
        print(f"Words remaining: {len(game.remaining_words())}  "
              f"(Hints left: {game.hints_available})")
    def show_message(self, text):
        print(text)
    def show_help(self):
        print("""
How to play Strands:
  * Select cells that trace a strand of adjacent letters
    (horizontal, vertical or diagonal, no cell reused).
  * Submit a strand to spell a word; theme words get locked in.
  * Find the SPANGRAM: a theme word touching two opposite
    sides of the board.
Commands:
  hint          reveal a letter from an unfound word
  found         list the words found so far
  help          show this help
  quit          exit the game
Input formats for a strand:
  0,0 1,1 2,2   (row,col pairs, 0-based)
  A1 B2 C3      (column letter + 1-based row)
""")
    def parse_input(self, text):
        """Return ('command', name) | ('path', [(r,c),...]) | ('bad', reason)."""
        tokens = text.split()
        if len(tokens) == 1 and tokens[0].lower() in self.COMMANDS:
            return ("command", tokens[0].lower())
        cells = []
        for tok in tokens:
            m = re.match(r"^([0-9]+)\s*,\s*([0-9]+)$", tok)
            if m:
                cells.append((int(m.group(1)), int(m.group(2))))
                continue
            m = re.match(r"^([A-Za-z])([0-9]+)$", tok)
            if m:
                col = string.ascii_uppercase.index(m.group(1).upper())
                cells.append((int(m.group(2)) - 1, col))
                continue
            return ("bad", f"Could not understand token '{tok}'. "
                           "Use 'row,col' pairs or 'A1' style cells.")
        if not cells:
            return ("bad", "No cells given. Type 'help' for usage.")
        return ("path", cells)
    def show_found(self, puzzle, game):
        found = game.found_words
        remaining = game.remaining_words()
        print("Found so far:")
        if found:
            for w in found:
                tag = " (SPANGRAM)" if w == puzzle.spangram else ""
                print(f"  - {w}{tag}")
        else:
            print("  (none yet)")
        print(f"Remaining: {len(remaining)} word(s).")
    def show_victory(self, puzzle, game):
        print(self._c("green", "=" * 60))
        print(self._c("green", f"  Puzzle complete: {puzzle.name}!"))
        print("  All strands merged:")
        for w in puzzle.all_words():
            tag = " (SPANGRAM)" if w == puzzle.spangram else ""
            print(f"    - {w}{tag}")
        print(self._c("green", "=" * 60))