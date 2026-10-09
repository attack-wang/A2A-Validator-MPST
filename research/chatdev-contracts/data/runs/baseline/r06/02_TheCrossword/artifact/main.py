'''
crossword.py - Interactive crossword puzzle (command-line application).
Features:
* Renders a grid of squares (with clue numbers) for across/down entries.
* The user enters a word by typing its clue number and direction
  (e.g. "1 across" or "2 down").
* Each entry is validated letter-by-letter against the solution;
  mismatches are reported without revealing the answer.
* When every word is correctly filled in, completion is confirmed.
Run:  python crossword.py
'''
# Alias table so users may type 'a'/'d' instead of 'across'/'down'.
DIRECTION_ALIASES = {"across": "across", "down": "down", "a": "across", "d": "down"}
class Word:
    """One crossword entry (an across or down answer)."""
    def __init__(self, number, direction, row, col, answer, clue):
        """Store the entry's position, answer and clue text."""
        self.number = number            # clue number shown in the grid
        self.direction = direction      # "across" or "down"
        self.row = row                  # row of the first letter
        self.col = col                  # column of the first letter
        self.answer = answer.upper()    # correct answer
        self.clue = clue                # hint shown to the player
        self.filled = False             # True once correctly entered
    @property
    def length(self):
        """Number of letters in the answer."""
        return len(self.answer)
    def cells(self):
        """Yield the (row, col) coordinate of every letter of this word."""
        for i in range(self.length):
            if self.direction == "across":
                yield self.row, self.col + i
            else:
                yield self.row + i, self.col
    def key(self):
        """Identifier used in prompts, e.g. '1 across'."""
        return f"{self.number} {self.direction}"
class Crossword:
    """Holds the solution grid, the player's grid and all word entries."""
    def __init__(self, solution, words):
        """Build the player grid from the solution ('.' = blocked square)."""
        self.solution = [list(row) for row in solution]
        self.rows = len(self.solution)
        self.cols = len(self.solution[0])
        self.words = words
        # Player grid: None = empty, otherwise a correctly placed letter.
        self.grid = [[None] * self.cols for _ in range(self.rows)]
        # Map (row, col) -> clue number for squares that start an entry.
        self.start_numbers = {(w.row, w.col): w.number for w in words}
    def display(self):
        """Print the grid with indices, clue numbers and current letters."""
        print("    " + " ".join(str(c) for c in range(self.cols)))
        for r in range(self.rows):
            row_cells = []
            for c in range(self.cols):
                if self.solution[r][c] == ".":
                    row_cells.append("#")                                # blocked square
                elif self.grid[r][c] is not None:
                    row_cells.append(self.grid[r][c])                    # filled letter
                elif (r, c) in self.start_numbers:
                    row_cells.append(str(self.start_numbers[(r, c)]))    # clue number
                else:
                    row_cells.append("_")                                # empty square
            print(f" {r}: " + " ".join(row_cells))
        print()
    def print_clues(self):
        """Print the across and down clue lists with solved markers."""
        for direction in ("across", "down"):
            print(direction.upper())
            for w in self.words:
                if w.direction == direction:
                    mark = "  [SOLVED]" if w.filled else ""
                    print(f"  {w.number}. {w.clue} ({w.length} letters){mark}")
        print()
    def find_word(self, number, direction):
        """Return the Word with the given number and direction, or None."""
        for w in self.words:
            if w.number == number and w.direction == direction:
                return w
        return None
    def try_fill(self, word, guess):
        """
        Validate a guess letter-by-letter against the solution.
        Returns (ok, errors): ok is True when the guess is fully correct
        (the word is then written into the grid); errors is a list of
        human-readable messages explaining every mismatch found.
        """
        guess = guess.upper().replace(" ", "")
        if len(guess) != word.length:
            return False, [f"Expected {word.length} letters, got {len(guess)}."]
        errors = []
        for i, (r, c) in enumerate(word.cells()):
            existing = self.grid[r][c]  # letter placed by a crossing word
            if existing is not None and existing != guess[i]:
                errors.append(
                    f"Letter {i + 1} conflicts with '{existing}' already in the grid."
                )
            elif guess[i] != self.solution[r][c]:
                errors.append(f"Letter {i + 1} is incorrect.")
        if errors:
            return False, errors
        # All letters match: write them into the player's grid.
        for i, (r, c) in enumerate(word.cells()):
            self.grid[r][c] = guess[i]
        word.filled = True
        return True, []
    def is_complete(self):
        """True when every word has been correctly filled in."""
        return all(w.filled for w in self.words)
def parse_entry(text):
    """Split input like '1 across' or '2 d' into (number, direction)."""
    parts = text.strip().lower().split()
    if len(parts) != 2 or parts[1] not in DIRECTION_ALIASES:
        return None
    try:
        number = int(parts[0])
    except ValueError:
        return None
    return number, DIRECTION_ALIASES[parts[1]]
def build_puzzle():
    """Create the demo puzzle: solution grid and word entries."""
    solution = [
        "PYTHON",
        "R...U.",
        "I...T.",
        "N...P.",
        "T...U.",
        "....T.",
    ]
    words = [
        Word(1, "across", 0, 0, "PYTHON",
             "A popular programming language named after a comedy troupe"),
        Word(1, "down", 0, 0, "PRINT",
             "Built-in function that displays text on the screen"),
        Word(2, "down", 0, 4, "OUTPUT",
             "What a program produces after it runs"),
    ]
    return Crossword(solution, words)
def main():
    """Entry point: build the puzzle and run the input loop."""
    puzzle = build_puzzle()
    print("=" * 46)
    print("              CROSSWORD PUZZLE")
    print("=" * 46)
    puzzle.display()
    puzzle.print_clues()
    print("Enter a word by its clue number and direction,")
    print("e.g. '1 across' or '2 down'. Type 'quit' to exit.")
    print("-" * 46)
    while not puzzle.is_complete():
        entry = input("Clue (number + direction): ").strip()
        if entry.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            return
        parsed = parse_entry(entry)
        if parsed is None:
            print("Invalid input. Use: <number> <across|down>\n")
            continue
        number, direction = parsed
        word = puzzle.find_word(number, direction)
        if word is None:
            print(f"No {direction} entry number {number}. Try again.\n")
            continue
        if word.filled:
            print(f"'{word.key()}' is already solved.\n")
            continue
        # Show the clue and the letters already known from crossings.
        pattern = "".join(
            puzzle.grid[r][c] if puzzle.grid[r][c] else "_"
            for (r, c) in word.cells()
        )
        print(f"Clue {word.key()}: {word.clue}")
        print(f"Current: {pattern}  ({word.length} letters)")
        guess = input("Your answer: ").strip()
        if not guess:
            print("No answer given.\n")
            continue
        ok, errors = puzzle.try_fill(word, guess)
        if ok:
            print("Correct! Word filled in.\n")
        else:
            print("Sorry, that entry is not correct:")
            for e in errors:
                print(f"  - {e}")
            print()
        puzzle.display()
        puzzle.print_clues()
    print("=" * 46)
    print("  Congratulations! You completed the crossword!")
    print("=" * 46)
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")