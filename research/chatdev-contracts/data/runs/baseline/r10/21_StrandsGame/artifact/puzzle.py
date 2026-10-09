class Target:
    def __init__(self, phrase, is_key=False):
        self.phrase = phrase
        self.is_key = is_key
        self.found = False
        self.found_by = []  # strand ids used
    @property
    def normalized(self): ...
class Puzzle:
    def __init__(self, pid, theme, description, strand_texts, target_specs, bonus_words):
        build strands with ids 1..n
        build targets
        self.hints_used = 0
        self.invalid_attempts = 0
        self.valid_merges = 0
    def get_strand(self, sid)
    def attempt_merge(self, strand_ids) -> MergeResult
    def is_complete(self)
    def progress(self) -> (found_count, total)
    def hint(self) -> str
    def undo_last(self) -> bool