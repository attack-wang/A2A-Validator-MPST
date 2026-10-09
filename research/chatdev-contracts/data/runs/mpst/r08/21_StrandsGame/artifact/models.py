'''
models.py
Core data models for the Strands word-segmentation puzzle.
Strand      -- a single piece of text that the player may select and merge.
MergeResult -- the outcome of a merge attempt, consumed by the game loop
               to produce feedback, scoring and completion checks.
'''
from dataclasses import dataclass, field
@dataclass
class Strand:
    """One selectable fragment of text on the board.
    Attributes:
        id:   Unique identifier (unique per strand occurrence, e.g. "S1", "S2").
        text: The uppercase fragment the player sees and selects.
        used: True once this strand has been consumed by a valid merge.
    """
    id: str
    text: str
    used: bool = False
# Possible statuses carried by MergeResult:
#   valid          -- a target word merged with its correct strands
#   core           -- the special "spangram-like" core word merged correctly
#   bonus          -- a dictionary-valid word that is not a target (small points)
#   invalid        -- the concatenation is not a word at all
#   too_few        -- fewer than two strands selected
#   used_strand    -- a selected strand has already been merged
#   duplicate      -- the same strand selected more than once
#   unknown_strand -- a selected id does not exist on the board
#   wrong_strands  -- correct spelling, but the strands belong to other words
#   already_found  -- the word was already merged earlier
@dataclass
class MergeResult:
    """Outcome of a merge attempt, consumed by the game loop for feedback."""
    status: str
    word: str = ""
    points: int = 0
    message: str = ""
    @property
    def success(self) -> bool:
        """True when the merge consumed strands (valid, core or bonus)."""
        return self.status in ("valid", "core", "bonus")