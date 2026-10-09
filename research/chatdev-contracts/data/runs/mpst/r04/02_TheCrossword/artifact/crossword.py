class Crossword:
    def __init__(self, size, words):
        self.size = size
        self.words = list(words)
        self.solution = [[None] * size for _ in range(size)]
        self.grid = [[None] * size for _ in range(size)]
        self._build_solution()
    def _build_solution(self):
        for word in self.words:
            for i, (r, c) in enumerate(word.cells()):
                letter = word.answer[i].upper()
                if self.solution[r][c] is not None and self.solution[r][c] != letter:
                    raise ValueError(f"Inconsistent puzzle data at ({r},{c})")
                self.solution[r][c] = letter
    def is_block(self, row, col):
        return self.solution[row][col] is None
    def get_letter(self, row, col):
        return self.grid[row][col]
    def set_letter(self, row, col, letter):
        self.grid[row][col] = letter
    def find_word(self, number, direction):
        for word in self.words:
            if word.number == number and word.direction == direction:
                return word
        return None
    def validate_entry(self, word, guess):
        """
        Validate a guessed word against the solution and existing entries.
        Returns (ok, errors) where errors is a list of messages.
        """
        guess = guess.upper()
        errors = []
        if len(guess) != word.length:
            errors.append(f"Expected {word.length} letters, got {len(guess)}.")
            return False, errors
        for i, (r, c) in enumerate(word.cells()):
            letter = guess[i]
            solution_letter = self.solution[r][c]
            existing = self.grid[r][c]
            if letter != solution_letter:
                errors.append(f"Letter {i+1} ('{letter}') does not match the solution.")
            elif existing is not None and existing != letter:
                errors.append(f"Letter {i+1} conflicts with an intersecting word.")
        return (not errors), errors
    def place_word(self, word, guess):
        """Place a validated word into the grid."""
        guess = guess.upper()
        for i, (r, c) in enumerate(word.cells()):
            self.grid[r][c] = guess[i]
    def clear_word(self, word):
        """Clear letters of a word, but only those not shared with other filled words."""
        shared = set()
        for other in self.words:
            if other is word:
                continue
            # if other word is fully filled, its letters are protected
            if self.is_word_filled(other):
                shared.update(other.cells())
        for (r, c) in word.cells():
            if (r, c) not in shared:
                self.grid[r][c] = None
    def is_word_filled(self, word):
        return all(self.grid[r][c] is not None for (r, c) in word.cells())
    def is_word_correct(self, word):
        return all(self.grid[r][c] == self.solution[r][c] for (r, c) in word.cells())
    def is_complete(self):
        return all(self.is_word_correct(w) for w in self.words)
    def progress(self):
        filled = sum(1 for w in self.words if self.is_word_filled(w))
        correct = sum(1 for w in self.words if self.is_word_correct(w))
        return filled, correct, len(self.words)