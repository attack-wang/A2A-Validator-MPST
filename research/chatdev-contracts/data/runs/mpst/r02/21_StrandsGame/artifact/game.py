class StrandsGame:
    def __init__(self, puzzle):
        self.title = puzzle["title"]
        self.theme = puzzle["theme"]
        self.hint_text = puzzle["hint_text"]
        self.strands = [Strand(t) for t in puzzle["strands"]]
        self.answers = [Answer(a["word"], a["segments"]) for a in puzzle["answers"]]
        self.solved_answers = []
        # verify solvability at load time
        if not self._can_partition(...):
            raise ValueError(...)