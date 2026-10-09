class MergeResult:  # or enum + dataclass
    status: VALID_TARGET / ALREADY_FOUND / BONUS_WORD / INVALID / ERROR
    phrase: str
    target: Optional[Target]
    message details
class MergeValidator:
    def __init__(self, bonus_words): ...
    def validate(self, puzzle, strand_ids) -> MergeResult