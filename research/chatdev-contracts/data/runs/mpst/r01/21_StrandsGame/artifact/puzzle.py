'''
puzzle.py
Defines the Puzzle data model and the built-in puzzle library for the
Strands word-segmentation game.
A Puzzle is declared as a theme plus a list of solutions. Each solution
pairs a target phrase with the ordered strand fragments whose concatenation
forms that phrase. The playable strand pool is derived automatically by
flattening every solution's fragments, which guarantees that solving all
targets consumes every strand exactly once.
Fixes applied per test report:
- Bug #5: PUZZLE_LIBRARY now contains real, fully playable puzzles instead
  of the '...' placeholder.
'''
from dataclasses import dataclass
from typing import List, Tuple
@dataclass(frozen=True)
class Solution:
    """A target phrase and the ordered strand fragments that build it."""
    phrase: str
    fragments: Tuple[str, ...]
    @property
    def strand_count(self) -> int:
        return len(self.fragments)
@dataclass
class Puzzle:
    """A complete Strands level: theme, solutions, and derived strand pool."""
    theme: str
    solutions: List[Solution]
    def __post_init__(self):
        # derive pool
        self.strand_pool: List[str] = [frag for sol in self.solutions for frag in sol.fragments]
    @property
    def total_strands(self) -> int:
        return len(self.strand_pool)
    @property
    def target_count(self) -> int:
        return len(self.solutions)
def _solutions(*pairs: Tuple[str, List[str]]) -> List[Solution]:
    return [Solution(phrase=p, fragments=tuple(fr)) for p, fr in pairs]
PUZZLE_LIBRARY: List[Puzzle] = [
    Puzzle(
        theme="Insects in Disguise",
        solutions=_solutions(
            ("BUTTERFLY", ["BUT", "TER", "FLY"]),
            ("DRAGONFLY", ["DRAG", "ON", "FLY"]),
            ("LADYBUG", ["LADY", "BUG"]),
            ("FIREFLY", ["FIRE", "FLY"]),
        ),
    ),
    Puzzle(
        theme="Out in Space",
        solutions=_solutions(
            ("SATELLITE", ["SAT", "ELL", "ITE"]),
            ("ASTEROID", ["ASTER", "OID"]),
            ("ROCKET", ["ROC", "KET"]),
            ("COMET", ["COM", "ET"]),
            ("NEBULA", ["NEB", "ULA"]),
        ),
    ),
    Puzzle(
        theme="In the Kitchen",
        solutions=_solutions(
            ("MICROWAVE", ["MICRO", "WAVE"]),
            ("SPATULA", ["SPAT", "ULA"]),
            ("TOASTER", ["TOAST", "ER"]),
            ("BLENDER", ["BLEND", "ER"]),
            ("LADLE", ["LAD", "LE"]),
        ),
    ),
    Puzzle(
        theme="Musical Instruments",
        solutions=_solutions(
            ("PIANO", ["PIA", "NO"]),
            ("GUITAR", ["GUI", "TAR"]),
            ("VIOLIN", ["VIO", "LIN"]),
            ("TRUMPET", ["TRUM", "PET"]),
            ("BANJO", ["BAN", "JO"]),
        ),
    ),
]