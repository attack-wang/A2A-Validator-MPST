'''
Crossword Puzzle - console application.
Features
--------
* Renders a grid of squares ('#' = blocked, '_' = empty, letters = filled).
* Shows numbered clues for the ACROSS and DOWN entries.
* The user plays a word by typing the clue number and direction,
  e.g. "2 across" or "3 down" (also accepts "2a", "2 down", ...).
* Every attempt is validated: the word length must match the entry,
  each letter must agree with letters already placed in crossing
  squares, and each letter must match the intended solution.
* When every open square holds the correct letter the program
  congratulates the player and terminates.
Run with:  python main.py
'''
import re
import sys
# ---------------------------------------------------------------------------
# Puzzle definition
# ---------------------------------------------------------------------------
# Completed (solution) grid. '#' marks a blocked square.
SOLUTION_GRID = [
    ['#', '#', 'P', '#', '#'],
    ['#', '#', 'A', '#', '#'],
    ['T', 'H', 'I', 'N', 'G'],
    ['E', 'O', 'N', '#', '#'],
    ['N', 'E', 'T', '#', '#'],
]
# Entries: clue number, direction, start row, start column, answer, clue text.
ENTRIES = [
    {'number': 1, 'direction': 'down',   'row': 0, 'col': 2,
     'answer': 'PAINT', 'clue': 'Apply colour to a canvas'},
    {'number': 2, 'direction': 'across', 'row': 2, 'col': 0,
     'answer': 'THING', 'clue': 'An object; any material entity'},
    {'number': 2, 'direction': 'down',   'row': 2, 'col': 0,
     'answer': 'TEN',   'clue': 'The number after nine'},
    {'number': 3, 'direction': 'down',   'row': 2, 'col': 1,
     'answer': 'HOE',   'clue': 'Garden tool used for weeding'},
    {'number': 4, 'direction': 'across', 'row': 3, 'col': 0,
     'answer': 'EON',   'clue': 'An indefinitely vast period of time'},
    {'number': 5, 'direction': 'across', 'row': 4, 'col': 0,
     'answer': 'NET',   'clue': 'Meshed trap for catching fish'},
]
# Accepted move syntax, e.g. "2 across", "2 ACROSS", "2a", "3 down", "3d".
MOVE_PATTERN = re.compile(r'^\s*(\d+)\s*(across|down|a|d)?\s*$', re.IGNORECASE)
class CrosswordPuzzle:
    '''Holds the puzzle state and implements the game logic.'''
    def __init__(self, solution_grid, entries):
        self.solution = [list(row) for row in solution_grid]
        self.entries = entries
        self.rows = len(self.solution)
        self.cols = len(self.solution[0]) if self.rows else 0
        # Player's grid: '#' for blocked squares, None for empty squares.
        self.grid = [[cell if cell == '#' else None for cell in row]
                     for row in self.solution]
        # Quick lookup: (clue number, direction) -> entry.
        self.lookup = {(e['number'], e['direction']): e for e in entries}
        self._validate_puzzle()
    # -- setup helpers ------------------------------------------------------
    def _validate_puzzle(self):
        '''Sanity-check the puzzle data so a broken definition fails fast.'''
        for entry in self.entries:
            for i, (row, col) in enumerate(self.entry_cells(entry)):
                if not (0 <= row < self.rows and 0 <= col < self.cols):
                    raise ValueError(
                        f"Entry {entry['number']} {entry['direction']} "
                        f"extends outside the grid.")
                if self.solution[row][col] != entry['answer'][i]:
                    raise ValueError(
                        f"Entry {entry['number']} {entry['direction']} "
                        f"conflicts with the solution grid at "
                        f"row {row}, col {col}.")
    def entry_cells(self, entry):
        '''Return the list of (row, col) squares covered by an entry.'''
        step_row, step_col = (0, 1) if entry['direction'] == 'across' else (1, 0)
        return [(entry['row'] + step_row * i, entry['col'] + step_col * i)
                for i in range(len(entry['answer']))]
    # -- display helpers ----------------------------------------------------
    def display_grid(self):
        '''Print the current grid ('#' blocked, '_' empty, letters filled).'''
        header = '     ' + ' '.join(str(col) for col in range(self.cols))
        print(header)
        for row in range(self.rows):
            cells = []
            for col in range(self.cols):
                cell = self.grid[row][col]
                cells.append('#' if cell == '#' else (cell or '_'))
            print(f'  {row}  ' + ' '.join(cells))
        print()
    def print_clues(self):
        '''Print the numbered across and down clues.'''
        for direction, title in (('across', 'ACROSS'), ('down', 'DOWN')):
            print(title)
            picked = sorted((e for e in self.entries
                             if e['direction'] == direction),
                            key=lambda e: e['number'])
            for entry in picked:
                print(f"  {entry['number']}. {entry['clue']} "
                      f"({len(entry['answer'])} letters)")
            print()
    # -- game logic ----------------------------------------------------------
    def parse_move(self, text):
        '''Parse "2 across" / "2a" / "3 down" ... -> (number, direction).'''
        match = MOVE_PATTERN.match(text)
        if match is None or match.group(2) is None:
            return None
        direction = 'across' if match.group(2).lower().startswith('a') else 'down'
        return int(match.group(1)), direction
    def place_word(self, entry, word):
        '''Validate `word` for `entry`; place it if valid.
        Returns (success, message).
        '''
        word = word.upper()
        expected = len(entry['answer'])
        if len(word) != expected:
            return False, (f"'{word}' has {len(word)} letters, but "
                           f"{entry['number']} {entry['direction']} needs "
                           f"{expected}.")
        cells = self.entry_cells(entry)
        # 1) Letters must agree with letters already placed in crossings.
        for i, (row, col) in enumerate(cells):
            existing = self.grid[row][col]
            if existing is not None and existing != word[i]:
                return False, (f"Letter '{word[i]}' at position {i + 1} "
                               f"conflicts with '{existing}' already in the "
                               f"grid at row {row}, col {col}.")
        # 2) Letters must match the intended solution.
        for i, (row, col) in enumerate(cells):
            if self.solution[row][col] != word[i]:
                return False, (f"'{word}' is not the correct answer for "
                               f"{entry['number']} {entry['direction']}.")
        # Valid: write the letters into the grid.
        for i, (row, col) in enumerate(cells):
            self.grid[row][col] = word[i]
        return True, (f"Placed {word} in {entry['number']} "
                      f"{entry['direction']}.")
    def is_complete(self):
        '''True when every open square holds the correct letter.'''
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] != self.solution[row][col]:
                    return False
        return True
    # -- main loop ------------------------------------------------------------
    def play(self):
        '''Run the interactive game loop until solved or quit.'''
        print('=' * 46)
        print('        WELCOME TO THE CROSSWORD PUZZLE')
        print('=' * 46)
        self.display_grid()
        self.print_clues()
        print("Enter a clue number and direction, e.g. '2 across' or '3 down'.")
        print("Commands: 'clues' = show clues, 'grid' = redraw grid, "
              "'quit' = exit.")
        while True:
            try:
                raw = input('\nYour move: ').strip()
            except (EOFError, KeyboardInterrupt):
                print('\nThanks for playing - goodbye!')
                return
            if not raw:
                continue
            command = raw.lower()
            if command in ('quit', 'exit', 'q'):
                print('Thanks for playing - goodbye!')
                return
            if command == 'clues':
                self.print_clues()
                continue
            if command == 'grid':
                self.display_grid()
                continue
            move = self.parse_move(raw)
            if move is None:
                print("Invalid input. Use '<number> <across|down>', "
                      "e.g. '2 across' or '3 down'.")
                continue
            number, direction = move
            entry = self.lookup.get((number, direction))
            if entry is None:
                valid = sorted(n for (n, d) in self.lookup if d == direction)
                print(f"There is no {number} {direction} entry. "
                      f"Valid {direction} numbers: {valid}.")
                continue
            cells = self.entry_cells(entry)
            current = ''.join(self.grid[row][col] or '_'
                              for row, col in cells)
            print(f"\n{number} {direction.upper()}: {entry['clue']} "
                  f"({len(entry['answer'])} letters)")
            print(f"Currently: {current}")
            try:
                word = input('Enter your word: ').strip()
            except (EOFError, KeyboardInterrupt):
                print('\nThanks for playing - goodbye!')
                return
            if not word:
                print('No word entered - move cancelled.')
                continue
            success, message = self.place_word(entry, word)
            print(message)
            if success:
                self.display_grid()
                if self.is_complete():
                    print('*' * 46)
                    print('   CONGRATULATIONS! You solved the crossword!')
                    print('*' * 46)
                    return
def main():
    '''Create the puzzle and start the game loop.'''
    CrosswordPuzzle(SOLUTION_GRID, ENTRIES).play()
if __name__ == '__main__':
    main()