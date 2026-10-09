'''
game.py
StrandsGame: runtime state and rules engine for a Puzzle.
Tracks found words, claimed cells, hint reveals, and verifies
strand submissions against the puzzle's theme words and spangram.
'''
import random
class StrandsGame:
    """Runtime game state: found words, claimed cells, hints."""
    def __init__(self, puzzle, max_hints=3):
        self.puzzle = puzzle
        self.found_words = []
        self.claimed = set()
        self.revealed_cells = set()
        self.hints_available = max_hints
    def remaining_words(self):
        return [w for w in self.puzzle.all_words() if w not in self.found_words]
    def claimed_cells(self):
        return set(self.claimed)
    def is_complete(self):
        return not self.remaining_words()
    def _path_for(self, target):
        """Find a legal adjacent-cell path spelling `target` (DFS)."""
        def search(cell, idx, path):
            r, c = cell
            if self.puzzle.letter_at(r, c) != target[idx]:
                return None
            path = path + [cell]
            if idx == len(target) - 1:
                return path
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if self.puzzle.in_bounds(nr, nc) and (nr, nc) not in path:
                        result = search((nr, nc), idx + 1, path)
                        if result:
                            return path if False else result
            return None
        for r in range(self.puzzle.rows):
            for c in range(self.puzzle.cols):
                path = search((r, c), 0, [])
                if path:
                    return path
        return None
    def submit_path(self, path):
        if not path or not self.puzzle.is_valid_path(path):
            return {"message": "Invalid strand: cells must be adjacent, no repeats.",
                    "complete": False}
        word = self.puzzle.word_for_path(path)
        if len(word) < 3:
            return {"message": "Strands must be at least 3 letters.", "complete": False}
        kind = self.puzzle.classify(word, path)
        if kind == "spangram":
            self.found_words.append(word)
            self.claimed.update(path)
            msg = f"SPANGRAM! You found '{word}'."
        elif kind == "spangram_short":
            msg = (f"'{word}' is the spangram, but it must touch two "
                   "opposite sides of the board.")
        elif kind == "theme":
            self.found_words.append(word)
            self.claimed.update(path)
            msg = f"Nice! '{word}' is a theme word."
        elif kind == "non_theme":
            msg = f"'{word}' is a word, but not part of the theme."
        else:
            msg = f"'{word}' is not a valid word."
        return {"message": msg, "complete": self.is_complete()}
    def use_hint(self):
        if self.hints_available <= 0:
            return ("No hints available. ...", None)
        remaining = self.remaining_words()
        if not remaining:
            return ("Puzzle already complete - no hints needed.", None)
        words = remaining[:]
        random.shuffle(words)
        for word in words:
            path = self._path_for(word)
            if not path:
                continue
            claimed = self.claimed_cells()
            candidates = [cell for cell in path
                          if cell not in self.revealed_cells
                          and cell not in claimed]
            if not candidates:
                candidates = [cell for cell in path
                              if cell not in self.revealed_cells]
            if not candidates:
                continue
            cell = random.choice(candidates)
            self.revealed_cells.add(cell)
            self.hints_available -= 1
            r, c = cell
            letter = self.puzzle.letter_at(r, c)
            return (f"Hint: the letter '{letter}' at row {r}, col {c} "
                    f"belongs to an unfound theme word.", cell)
        return ("No new letters left to reveal.", None)