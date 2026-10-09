class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.solution = None  # correct letter, None for block
        self.letter = None    # currently entered letter
        self.number = None    # clue number if a word starts here
        self.is_block = True  # False if usable
    @property
    def is_open(self):
        return not self.is_block
    def fill(self, letter):
        if self.is_block:
            raise CrosswordError(f"Cell ({self.row}, {self.col}) is a blocked square.")
        letter = str(letter).strip().upper()
        if len(letter) != 1 or not ("A" <= letter <= "Z"):
            raise CrosswordError(f"{letter!r} is not a single letter A-Z.")
        self.letter = letter
    def clear(self):
        self.letter = None
    def is_correct(self):
        if self.is_block:
            return True
        return self.letter == self.solution
    def is_empty(self):
        return self.letter is None
    def display(self):
        """Show the clue number (if any) when empty, else the current letter."""
        if self.is_block:
            return "■" or something