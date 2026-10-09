class MergeValidator:
    BONUS_SCORE = 5
    def __init__(self, dictionary): self.dictionary = {w.upper() for w in dictionary}
    def validate(self, merge_text, puzzle, found_targets):
        returns dict/tuple (status, message)
        statuses: VALID, DUPLICATE, BONUS, PARTIAL, INVALID