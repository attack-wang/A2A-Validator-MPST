class Entry:
    def __init__(self, direction, row, col, answer, clue, number=None):
        self.direction = Direction(direction) if isinstance(direction, str) else direction
        self.row = row
        self.col = col
        self.answer = answer.strip().upper()
        self.clue = clue
        self.number = number
        self.cells = []
    @property
    def length(self):
        return len(self.answer)
    @property
    def label(self):
        return f"{self.number}-{self.direction.label}"
    def is_filled(self):
        return all(not c.is_empty() for c in self.cells)
    def is_correct(self):
        return all(c.is_correct() for c in self.cells)
    def pattern(self):
        return "".join(c.letter if c.letter else "." for c in self.cells)
    def __repr__(self):
        return f"<Entry {self.label}: {self.pattern()} (answer {self.answer})>"