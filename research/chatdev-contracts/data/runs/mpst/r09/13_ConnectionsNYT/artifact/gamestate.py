class GameState:
    MAX_MISTAKES = 4
    GROUP_SIZE = 4
    def __init__(self, puzzle):
        self.categories = puzzle["categories"]
        self.word_to_category = {}
        for cat in self.categories:
            for w in cat["words"]:
                self.word_to_category[w] = cat["name"]
        self.words = list(puzzle["words"])  # current grid order
        self.selected = []
        self.found = []  # list of category names in order found
        self.mistakes = 0
        self.game_over = False
        self.won = False
    def toggle_select(self, word):
        if self.game_over: return False
        if word in self.found_words(): return False
        if word in self.selected:
            self.selected.remove(word); return True
        if len(self.selected) >= self.GROUP_SIZE: return False
        self.selected.append(word); return True
    def clear_selection(self):
        self.selected = []
    def shuffle_remaining(self):
        found_words = self.found_words()
        remaining = [w for w in self.words if w not in found_words]
        random.shuffle(remaining)
        self.words = remaining
        return self.words