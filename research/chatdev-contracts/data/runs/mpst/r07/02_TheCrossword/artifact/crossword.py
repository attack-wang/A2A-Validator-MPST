'''
crossword.py -- Interactive crossword puzzle.
The puzzle is displayed as a grid of squares. The user fills in words by
typing the clue number, a direction (A = across, D = down) and the word,
e.g. "1 A HEART". Every letter is validated against the solution (length
check, per-letter check and crossing-letter conflict check), and the
program congratulates the user once the whole grid is correctly filled.
Run:  python crossword.py
'''
# ---------------------------------------------------------------------------
# Puzzle definition: (clue number, start row, start col, direction, answer, clue)
# Rows and columns are 0-based internally, shown 1-based to the user.
# ---------------------------------------------------------------------------
GRID_SIZE = 5
ENTRIES = [
    (1, 0, 0, 'A', 'HEART', 'Organ that pumps blood'),
    (2, 0, 1, 'D', 'EMBER', 'Glowing fragment of a dying fire'),
    (3, 0, 4, 'D', 'TREES', 'Oaks and pines, for example'),
    (4, 2, 0, 'A', 'ABUSE', 'Mistreat or use improperly'),
    (5, 2, 0, 'D', 'ARM', 'Upper limb of the body'),
]
class Crossword:
    """Holds the crossword layout, the clues and the user's progress."""
    def __init__(self, size, entries):
        """Build the grid model from the puzzle definition."""
        self.size = size
        self.entries = {}                       # (number, direction) -> entry info
        for number, row, col, direction, answer, clue in entries:
            self.entries[(number, direction)] = {
                'number': number, 'row': row, 'col': col,
                'direction': direction, 'answer': answer, 'clue': clue,
            }
        self.solution = {}                      # (row, col) -> correct letter
        for entry in self.entries.values():
            for offset in range(len(entry['answer'])):
                r, c = self._cell(entry, offset)
                self.solution[(r, c)] = entry['answer'][offset]
        self.grid = {pos: '' for pos in self.solution}   # user's letters ('' = empty)
        self.starts = {}                        # (row, col) -> clue numbers starting there
        for entry in self.entries.values():
            pos = (entry['row'], entry['col'])
            self.starts.setdefault(pos, []).append(entry['number'])
    def _cell(self, entry, offset):
        """Return the (row, col) of the offset-th letter of an entry."""
        if entry['direction'] == 'A':
            return entry['row'], entry['col'] + offset
        return entry['row'] + offset, entry['col']
    def _cell_symbol(self, row, col):
        """Return the single symbol shown for a grid cell."""
        if (row, col) not in self.solution:
            return '#'                                   # blocked square
        letter = self.grid[(row, col)]
        if letter:
            return letter                                # filled letter square
        if (row, col) in self.starts:                    # empty square that starts a word
            label = '/'.join(str(n) for n in sorted(self.starts[(row, col)]))
            return label if len(label) <= 3 else str(min(self.starts[(row, col)]))
        return '_'                                       # empty letter square
    def display(self):
        """Print the grid with the user's letters and both clue lists."""
        filled = sum(1 for pos in self.solution if self.grid[pos])
        print('\n      ' + ''.join(f'{c + 1:>3} ' for c in range(self.size)))
        for r in range(self.size):
            line = f'{r + 1:>3} ' + ''.join(
                f'{self._cell_symbol(r, c):>3} ' for c in range(self.size))
            print(line.rstrip())
        print(f'\nProgress: {filled}/{len(self.solution)} letters filled.')
        print('\nAcross:')
        for (number, direction), entry in sorted(self.entries.items()):
            if direction == 'A':
                print(f'  {number}. {entry["clue"]} ({len(entry["answer"])} letters)')
        print('Down:')
        for (number, direction), entry in sorted(self.entries.items()):
            if direction == 'D':
                print(f'  {number}. {entry["clue"]} ({len(entry["answer"])} letters)')