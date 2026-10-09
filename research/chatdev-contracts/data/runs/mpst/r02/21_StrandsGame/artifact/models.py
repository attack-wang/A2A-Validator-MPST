class Strand:
    """A single text fragment the player can select and merge."""
    def __init__(self, text):
        self.text = text
        self.used = False
    @property
    def normalized(self):
        return normalize(self.text)
class Answer:
    """A target word the player must form by merging strands."""
    def __init__(self, word, segments):
        self.word = word
        self.segments = segments
        self.solved = False
    @property
    def normalized(self):
        return normalize(self.word)