'''
puzzle.py
Puzzle class: holds one puzzle's strands and answers, tracks game state,
processes merge attempts, provides hints, and detects completion.
'''
from utils import normalize
from validator import MergeValidator, MergeResult
class Puzzle:
    def __init__(self, definition):
        self.title = definition["title"]
        self.theme = definition["theme"]
        self.spangram = definition.get("spangram")
        self.answer_entries = list(definition["answers"])  # dicts: word + clue
        self.answers = [e["word"] for e in self.answer_entries]
        self.clues = {normalize(e["word"]): e["clue"] for e in self.answer_entries}
        self.strands = [{"text": s, "used": False} for s in definition["strands"]]
        self.found = []          # display words in the order found
        self.revealed = set()    # normalized answers whose clue has been shown
        self.validator = MergeValidator(self.answer_entries, self.spangram)
        self.attempts = 0
        self.valid_merges = 0
        self._decompositions = self._compute_decompositions()
    # ---- state helpers ----
    def remaining_strands(self):
        return [(i + 1, s["text"]) for i, s in enumerate(self.strands) if not s["used"]]
    def is_complete(self):
        return all(s["used"] for s in self.strands)
    def found_spangram(self):
        return normalize(self.spangram) in {normalize(w) for w in self.found} if self.spangram else False
    # ---- core mechanic ----
    def attempt_merge(self, indices):
        """Merge strands at the given ORIGINAL 1-based indices, in selection order."""
        if not indices or not all(isinstance(i, int) for i in indices):
            return MergeResult(MergeResult.INVALID, message="Please enter strand numbers, e.g. '1 2 3'.")
        seen = set()
        for i in indices:
            if not 1 <= i <= len(self.strands):
                return MergeResult(MergeResult.INVALID, message=f"Strand {i} does not exist (1-{len(self.strands)}).")
            if i in seen:
                return MergeResult(MergeResult.INVALID, message=f"Strand {i} selected twice.")
            seen.add(i)
            if self.strands[i - 1]["used"]:
                return MergeResult(MergeResult.ALREADY_FOUND, message=f"Strand {i} is already used.")
        candidate = "".join(self.strands[i - 1]["text"] for i in indices)
        result = self.validator.validate(candidate)
        self.attempts += 1
        if result.is_valid:
            for i in indices:
                self.strands[i - 1]["used"] = True
            self.found.append(result.word)
            self.valid_merges += 1
        return result
    # ---- hints ----
    def _compute_decompositions(self):
        """Backtracking search: assign remaining strands to remaining answers."""
        ...
    def get_hint(self):
        ...