class Puzzle:
    """Theme clue, spangram, theme words, and per-word cell placement."""
    def __init__(self, clue, spangram, words):
        self.clue = clue
        self.spangram = spangram.upper()
        self.words = [w.upper() for w in words]
        self.word_cells = {}   # word -> frozenset(cells), filled during build
        self.found_words = set()
        self.spangram_found = False
    @property total_words = len(self.words) + 1
    def is_theme(self, w): w in self.words
    def is_spangram(self, w)
    def found_count(self)
    def is_complete(self): spangram_found and len(found_words)==len(words)