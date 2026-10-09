'''
CrosswordPuzzle module: implements the crossword grid, clue list, word
entry validation and completion checking for the crossword game.
'''
GRID_SIZE = 7
# Layout: True = letter cell, False = black square.
LAYOUT = [
    [False, False, False, True,  False, False, False],
    [False, False, True,  True,  True,  True,  True ],
    [False, False, False, False, False, True,  False],
    [True,  True,  True,  True,  False, True,  False],
    [True,  False, True,  False, False, False, False],
    [True,  True,  True,  True,  True,  False, False],
    [False, False, True,  False, False, False, False],
]
SOLUTION = [
    [None,  None,  None,  'C',   None,  None,  None ],
    [None,  None,  'M',   'O',   'U',   'S',   'E'  ],
    [None,  None,  None,  None,  None,  'E',   None ],
    ['B',   'Y',   'T',   'E',   None,  'T',   None ],
    ['U',   None,  'R',   None,  None,  None,  None ],
    ['G',   'R',   'E',   'E',   'T',   None,  None ],
    [None,  None,  'E',   None,  None,  None,  None ],
]
ACROSS_CLUES = {
    2: "Pointing device you click (5 letters)",
    4: "Eight bits (4 letters)",
    6: "Say hello (5 letters)",
}
DOWN_CLUES = {
    1: "What programmers write (4 letters)",
    3: "Python collection with unique elements (3 letters)",
    4: "Program error, or a creepy crawler (3 letters)",
    5: "Data structure with branches, or a plant with a trunk (4 letters)",
}
ACROSS = "across"
DOWN = "down"
class Entry:
    """One crossword entry: clue number, direction, start cell and answer."""
    def __init__(self, number, direction, row, col, answer, clue):
        self.number = number
        self.direction = direction
        self.row = row
        self.col = col
        self.answer = answer.upper()
        self.clue = clue
    def cells(self):
        """Yield the (row, col) coordinates covered by this entry."""
        for i in range(len(self.answer)):
            if self.direction == ACROSS:
                yield (self.row, self.col + i)
            else:
                yield (self.row + i, self.col)
class CrosswordPuzzle:
    def __init__(self):
        self.size = GRID_SIZE
        self.layout = LAYOUT
        self.solution = SOLUTION
        self.user_grid = [[None] * self.size for _ in range(self.size)]
        self.entries = {}
        self.start_numbers = {}
        self._build_entries()
    def _build_entries(self):
        """Scan the layout and register every across/down entry."""
        number = 0
        for r in range(self.size):
            for c in range(self.size):
                if not self.layout[r][c]:
                    continue
                starts_across = (c == 0 or not self.layout[r][c - 1]) and \
                                (c + 1 < self.size and self.layout[r][c + 1])
                starts_down = (r == 0 or not self.layout[r - 1][c]) and \
                              (r + 1 < self.size and self.layout[r + 1][c])
                if not (starts_across or starts_down):
                    continue
                number += 1
                self.start_numbers[(r, c)] = number
                if starts_across:
                    length = 0
                    while c + length < self.size and self.layout[r][c + length]:
                        length += 1
                    answer = "".join(self.solution[r][c + i] for i in range(length))
                    self.entries[(number, ACROSS)] = Entry(
                        number, ACROSS, r, c, answer, ACROSS_CLUES[number])
                if starts_down:
                    length = 0
                    while r + length < self.size and self.layout[r + length][c]:
                        length += 1
                    answer = "".join(self.solution[r + i][c] for i in range(length))
                    self.entries[(number, DOWN)] = Entry(
                        number, DOWN, r, c, answer, DOWN_CLUES[number])
    def display(self):
        """Return the grid as a printable string."""
        lines = []
        header = "    " + "".join(f"  {c} " for c in range(self.size))
        lines.append(header)
        separator = "  +" + "---+" * self.size
        lines.append(separator)
        for r in range(self.size):
            row_str = f"{r} |"
            for c in range(self.size):
                row_str += f"{self._cell_text(r, c):^3}|"
            lines.append(row_str)
            lines.append(separator)
        return "\n".join(lines)
    def _cell_text(self, r, c):
        if not self.layout[r][c]:
            return "#"
        if self.user_grid[r][c] is not None:
            return self.user_grid[r][c]
        number = self.start_numbers.get((r, c))
        if number is not None:
            return str(number)
        return "_"
    def show_clues(self):
        """Return the across and down clue lists as a printable string."""
        lines = ["ACROSS:"]
        for (number, direction), entry in sorted(self.entries.items()):
            if direction == ACROSS:
                lines.append(f"  {number}. {entry.clue}")
        lines.append("DOWN:")
        for (number, direction), entry in sorted(self.entries.items()):
            if direction == DOWN:
                lines.append(f"  {number}. {entry.clue}")
        return "\n".join(lines)
    def get_entry(self, number, direction):
        """Return the Entry for (number, direction) or None."""
        return self.entries.get((number, direction))
    def enter_word(self, number, direction, word):
        """Write a word into the grid. Returns (success, message)."""
        entry = self.get_entry(number, direction)
        if entry is None:
            return False, f"No {direction} entry numbered {number}."
        word = word.strip().upper()
        if not word.isalpha():
            return False, "The word must contain letters only."
        if len(word) != len(entry.answer):
            return False, (f"Wrong length: entry {number} {direction} needs "
                           f"{len(entry.answer)} letters, you gave {len(word)}.")
        # Validate every letter against the solution (crossing letters included).
        for i, (r, c) in enumerate(entry.cells()):
            if self.solution[r][c] != word[i]:
                return False, (f"Letter '{word[i]}' does not match at position "
                               f"{i + 1} of entry {number} {direction}.")
        for i, (r, c) in enumerate(entry.cells()):
            self.user_grid[r][c] = word[i]
        return True, f"'{word}' fits entry {number} {direction}. {self.solved_count()} of {len(self.entries)} entries solved."
    def is_complete(self):
        """True when every letter cell holds the correct letter."""
        for r in range(self.size):
            for c in range(self.size):
                if self.layout[r][c] and self.user_grid[r][c] != self.solution[r][c]:
                    return False
        return True
    def solved_count(self):
        """Number of entries whose letters are all correctly filled."""
        count = 0
        for entry in self.entries.values():
            letters = [self.user_grid[r][c] for r, c in entry.cells()]
            if all(l == s for l, s in zip(letters, entry.answer)):
                count += 1
        return count