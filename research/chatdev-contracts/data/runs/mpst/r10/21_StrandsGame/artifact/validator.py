'''
validator.py
Defines MergeResult and MergeValidator.
...
'''
from utils import normalize
class MergeResult:
    """Record of a single merge attempt's outcome."""
    VALID = "valid"
    INVALID = "invalid"
    ALREADY_FOUND = "already_found"
    def __init__(self, status, word=None, is_spangram=False, message=""):
        self.status = status
        self.word = word
        self.is_spangram = is_spangram
        self.message = message
    @property
    def is_valid(self):
        return self.status == MergeResult.VALID
class MergeValidator:
    """Checks candidate strings against a puzzle's valid answers."""
    def __init__(self, answers, spangram=None):
        self._answers = {}
        for entry in answers:
            display = entry["word"] if isinstance(entry, dict) else entry
            self._answers[normalize(display)] = display
        self._spangram = normalize(spangram) if spangram else None
        self._found = set()
    def validate(self, candidate):
        key = normalize(candidate)
        if not key:
            return MergeResult(MergeResult.INVALID, message="Empty merge — nothing to check.")
        if key in self._found:
            display = self._answers[key]
            return MergeResult(MergeResult.ALREADY_FOUND, word=display,
                               message=f"'{display}' was already found!")
        if key in self._answers:
            display = self._answers[key]
            is_spangram = (key == self._spangram)
            self._found.add(key)
            if is_spangram:
                msg = f"★ SPANGRAM! '{display}' — you've spanned the theme!"
            else:
                msg = f"Valid merge! '{display}' is correct."
            return MergeResult(MergeResult.VALID, display, is_spangram, msg)
        return MergeResult(MergeResult.INVALID,
                           message=f"'{candidate.strip()}' is not a valid word or phrase. Try again!")