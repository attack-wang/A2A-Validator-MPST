'''
Crossword Puzzle - ChatDev console application.
A 7x7 crossword puzzle containing four interlocking words:
    1 Across : PROGRAM   (row 0)
    3 Across : MINIMUM   (row 6)
    1 Down   : PROBLEM   (column 0)
    2 Down   : MAXIMUM   (column 6)
Features:
    * Renders the grid of squares with row/column indices and prints the
      Across and Down clue lists.
    * The player fills in an entry with the command
          <clue number> <across|down> <word>      e.g.  1 across PROGRAM
    * Every letter is validated against the hidden solution; a wrong word
      is rejected and the grid is left unchanged.
    * When all squares are filled correctly the program congratulates the
      player and finishes.
Extra commands: grid, clues, help, quit/exit.
Run with:  python game.py
'''
from clue import Clue
class CrosswordGame:
    """Interactive crossword puzzle: grid state, rendering, validation and loop."""
    SIZE = 7
    BLOCK = "#"   # square not covered by any entry
    EMPTY = "_"   # square still to be filled by the player
    def __init__(self):
        """Build the hidden solution, the player grid and the clue list."""
        self.solution = [
            list("PROGRAM"),
            list("R#####A"),
            list("O#####X"),
            list("B#####I"),
            list("L#####M"),
            list("E#####U"),
            list("MINIMUM"),
        ]
        # Player grid: blocks stay blocks, fillable squares start empty.
        self.grid = [[self.BLOCK if letter == self.BLOCK else self.EMPTY
                      for letter in row] for row in self.solution]
        self.clues = [
            Clue(1, "ACROSS", 0, 0, "PROGRAM", "Code written by a developer"),
            Clue(1, "DOWN", 0, 0, "PROBLEM", "A difficult matter to solve"),
            Clue(2, "DOWN", 0, 6, "MAXIMUM", "The greatest possible amount"),
            Clue(3, "ACROSS", 6, 0, "MINIMUM", "The least possible amount"),
        ]
    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def render_grid(self):
        """Print the current grid with row/column indices and clue numbers."""
        start_numbers = {}
        for clue in self.clues:
            key = (clue.row, clue.col)
            if key not in start_numbers or clue.number < start_numbers[key]:
                start_numbers[key] = clue.number
        header = "     " + " ".join(str(c) for c in range(self.SIZE))
        lines = [header]
        for r in range(self.SIZE):
            row_cells = []
            for c in range(self.SIZE):
                cell = self.grid[r][c]
                if cell == self.EMPTY and (r, c) in start_numbers:
                    row_cells.append(str(start_numbers[(r, c)]))
                else:
                    row_cells.append(cell)
            lines.append(f"  {r}  " + " ".join(row_cells))
        print("\n".join(lines))
    def print_clues(self):
        """Print the Across and Down clue lists."""
        print("ACROSS")
        for clue in self.clues:
            if clue.direction == "ACROSS":
                print(f"  {clue.number}. {clue.hint} ({clue.length} letters)")
        print("DOWN")
        for clue in self.clues:
            if clue.direction == "DOWN":
                print(f"  {clue.number}. {clue.hint} ({clue.length} letters)")
    def print_help(self):
        """Print the list of supported commands."""
        print("Commands:")
        print("  <number> <across|down> <word>   fill an entry, e.g.  1 across PROGRAM")
        print("  grid    - show the current grid")
        print("  clues   - show the Across and Down clue lists")
        print("  help    - show this command list")
        print("  quit    - exit the game (alias: exit)")
    # ------------------------------------------------------------------
    # Game state helpers
    # ------------------------------------------------------------------
    def _find_clue(self, number, direction):
        """Return the Clue with the given number and direction, or None."""
        for clue in self.clues:
            if clue.number == number and clue.direction == direction:
                return clue
        return None
    def _is_clue_solved(self, clue):
        """bool: True when every square of the entry holds the correct letter."""
        return all(self.grid[row][col] == self.solution[row][col]
                   for row, col in clue.cells)
    def is_complete(self):
        """bool: True when every fillable square matches the hidden solution."""
        return all(self.grid[r][c] == self.solution[r][c]
                   for r in range(self.SIZE) for c in range(self.SIZE))
    def place_word(self, clue, word):
        """
        Validate 'word' against the clue's answer and write it into the grid.
        A word is accepted only when its length matches the entry and every
        letter matches the hidden solution letter-by-letter; otherwise the
        grid is left unchanged and the player is told where the first
        mismatch occurs.
        Returns:
            bool: True if the word was accepted and written, False otherwise.
        """
        if len(word) != clue.length:
            print(f"'{word}' has {len(word)} letters, but "
                  f"{clue.number} {clue.direction.lower()} needs {clue.length}.")
            return False
        if self._is_clue_solved(clue):
            if word == clue.answer:
                print(f"{clue.number} {clue.direction.lower()} is already filled in correctly.")
            else:
                print(f"{clue.number} {clue.direction.lower()} is already solved — "
                      f"'{word}' does not match.")
            return False
        for i, letter in enumerate(word):
            row, col = clue.cells[i]
            if letter != self.solution[row][col]:
                print(f"'{word}' does not fit {clue.number} {clue.direction.lower()} — "
                      f"letter {i + 1} is incorrect. The grid is unchanged.")
                return False
        for i, letter in enumerate(word):
            row, col = clue.cells[i]
            self.grid[row][col] = letter
        return True
    # ------------------------------------------------------------------
    # Command handling and main loop
    # ------------------------------------------------------------------
    def handle_command(self, raw):
        """
        Parse and execute one input line.
        Returns:
            bool: True to keep playing, False when the game should end
                  (player quit or puzzle completed).
        """
        text = raw.strip()
        if not text:
            return True
        lowered = text.lower()
        if lowered in ("quit", "exit"):
            print("Thanks for playing! Goodbye.")
            return False
        if lowered == "grid":
            self.render_grid()
            return True
        if lowered == "clues":
            self.print_clues()
            return True
        if lowered == "help":
            self.print_help()
            return True
        parts = text.split()
        if len(parts) != 3 or not parts[0].isdigit():
            print("Unknown command. Type 'help' for the command list.")
            return True
        number_text, direction_text, word = parts
        direction = direction_text.upper()
        if direction not in ("ACROSS", "DOWN"):
            print(f"Direction must be 'across' or 'down', not '{direction_text}'.")
            return True
        clue = self._find_clue(int(number_text), direction)
        if clue is None:
            print(f"There is no clue {number_text} {direction.lower()}. "
                  f"Type 'clues' to see the list.")
            return True
        word_upper = word.upper()
        if not word_upper.isalpha():
            print(f"'{word}' must contain letters only.")
            return True
        if self.place_word(clue, word_upper):
            print(f"{clue.number} {clue.direction.lower()} filled in with {word_upper}.")
            self.render_grid()
            if self.is_complete():
                print("\nCongratulations! You completed the crossword puzzle!")
                return False
        return True
    def run(self):
        """Start the interactive game loop."""
        print("=" * 60)
        print("Welcome to the ChatDev Crossword Puzzle!")
        print("=" * 60)
        self.print_clues()
        print()
        self.render_grid()
        print()
        self.print_help()
        while True:
            try:
                raw = input("\nEnter command> ")
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                return
            if not self.handle_command(raw):
                return