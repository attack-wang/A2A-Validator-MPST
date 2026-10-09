'''
game.py
Core state machine for a Strands puzzle session.
'''
import random
import time
from dataclasses import dataclass, field
from typing import List, Optional, Set, Tuple
from puzzle import Puzzle, Solution
from validator import MergeResult, MergeValidator, normalize
@dataclass
class Strand:
    uid: int
    text: str
    used: bool = False
    hinted: bool = False
@dataclass
class MergeRecord:
    phrase: str
    fragments: Tuple[str, ...]
    strand_uids: Tuple[int, ...]
class StrandsGame:
    """..."""
    def __init__(self, puzzle: Puzzle, seed: Optional[int] = None):
        self.puzzle = puzzle
        self.validator = MergeValidator(sol.phrase for sol in puzzle.solutions)
        self.solutions: List[Solution] = list(puzzle.solutions)
        self._found_norms: Set[str] = set()
        self.found: List[MergeRecord] = []
        self.selection: List[int] = []
        self.attempts = 0
        self.valid_merges = 0
        self.hints_used = 0
        self.started_at = time.time()
        self._rng = random.Random(seed)
        pool = puzzle.strand_pool[:]
        self._rng.shuffle(pool)
        self.strands: List[Strand] = [Strand(uid=i, text=text) for i, text in enumerate(pool)]
    # --- selection management ---
    def toggle_select(self, index: int) -> str:
        if index < 0 or index >= len(self.strands):
            return f"No strand at position {index + 1} — choose 1..{len(self.strands)}."
        strand = self.strands[index]
        if strand.used:
            return f"Strand '{strand.text}' is already merged — pick another."
        if index in self.selection:
            self.selection.remove(index)
            return f"Removed '{strand.text}' from selection."
        self.selection.append(index)
        return f"Added '{strand.text}' to selection."
    def clear_selection(self) -> str:
        count = len(self.selection)
        self.selection = []
        return "Selection cleared." if count else "Selection was already empty."
    def undo_selection(self) -> Optional[str]:
        if not self.selection:
            return None
        index = self.selection.pop()
        return self.strands[index].text
    def selection_fragments(self) -> List[str]:
        return [self.strands[i].text for i in self.selection]
    # --- validation ---
    def preview(self) -> Optional[MergeResult]:
        if not self.selection:
            return None
        return self.validator.validate(self.selection_fragments(), self._found_norms)
    def submit(self) -> MergeResult:
        fragments = self.selection_fragments()
        result = self.validator.validate(fragments, self._found_norms)
        self.attempts += 1
        if result.is_valid:
            uids = tuple(self.strands[i].uid for i in self.selection)
            for i in self.selection:
                self.strands[i].used = True
            record = MergeRecord(
                phrase=result.display_phrase,
                fragments=tuple(fragments),
                strand_uids=uids,
            )
            self.found.append(record)
            self._found_norms.add(normalize(result.display_phrase))
            self.valid_merges += 1
        self.selection = []
        return result
    # --- status ---
    def is_complete(self) -> bool:
        return len(self.found) == len(self.solutions)
    def progress(self) -> str:
        return f"{len(self.found)}/{len(self.solutions)}"
    def remaining_solutions(self) -> List[Solution]:
        return [s for s in self.solutions if normalize(s.phrase) not in self._found_norms]
    def get_hint(self) -> Optional[str]:
        remaining = self.remaining_solutions()
        if not remaining:
            return None
        solution = self._rng.choice(remaining)
        first = solution.fragments[0]
        for strand in self.strands:
            if strand.text == first and not strand.used:
                strand.hinted = True
                break
        self.hints_used += 1
        return (f"Hint: one unfound merge starts with the strand '{first}' "
                f"and uses {solution.strand_count} strand(s) in total.")