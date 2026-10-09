from enum import Enum
class MergeStatus(Enum):
    VALID_TARGET = "valid_target"
    VALID_WORD = "valid_word"
    INVALID = "invalid"
    ERROR = "error"
class MergeResult:
    def __init__(self, status, word=None, message="", target=None, used_strands=None, warning=None):
        ...
class MergeValidator:
    def __init__(self, dictionary):
        self.dictionary = dictionary
    def validate(self, puzzle, strands):
        # ERROR cases
        if not strands:
            return MergeResult(MergeStatus.ERROR, message="No strands selected...")
        used = [s for s in strands if not s.is_available]
        if used:
            return MergeResult(MergeStatus.ERROR, message=...)
        # duplicates check
        ids = [s.sid for s in strands]
        if len(ids) != len(set(ids)):
            return MergeResult(MergeStatus.ERROR, message="Duplicate strand in selection...")
        candidate = puzzle.normalize("".join(s.text for s in strands))
        target = puzzle.find_target(candidate)
        if target:
            return MergeResult(MergeStatus.VALID_TARGET, word=target, target=target, used_strands=strands)
        if candidate in self.dictionary:
            return MergeResult(MergeStatus.VALID_WORD, word=candidate, warning="Valid word, but not needed...")
        return MergeResult(MergeStatus.INVALID, message=f"'{candidate}' is not a valid merge.")