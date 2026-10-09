'''
validator.py
Merge validation for Strands...
'''
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Iterable, Set, Tuple
class MergeStatus(Enum):
    VALID = "valid"
    ALREADY_FOUND = "already_found"
    PARTIAL = "partial"
    INVALID = "invalid"
@dataclass
class MergeResult:
    status: MergeStatus
    phrase: str = ""
    display_phrase: str = ""
    message: str = ""
    fragments: Tuple[str, ...] = ()
    @property
    def is_valid(self) -> bool:
        return self.status is MergeStatus.VALID
def normalize(text: str) -> str:
    return "".join(text.split()).upper()
class MergeValidator:
    """Checks strand selections against the puzzle's target phrases."""
    def __init__(self, phrases: Iterable[str]):
        self._display: Dict[str, str] = {}
        self._prefixes: Set[str] = set()
        for phrase in phrases:
            norm = normalize(phrase)
            self._display[norm] = phrase
            norm_len = len(norm)
            for i in range(1, norm_len):
                self._prefixes.add(norm[:i])
    def validate(self, fragments: Iterable[str], found_norms: Set[str]) -> MergeResult:
        frags = tuple(fragments)
        if not frags:
            return MergeResult(MergeStatus.INVALID,
                               message="Selection is empty — select at least one strand.")
        candidate = normalize("".join(frags))
        display = self._display.get(candidate, candidate)
        if candidate in found_norms:
            return MergeResult(MergeStatus.ALREADY_FOUND, phrase=candidate,
                               display_phrase=display,
                               message=f"'{display}' has already been merged.")
        if candidate in self._display:
            return MergeResult(MergeStatus.VALID, phrase=candidate, display_phrase=display,
                               fragments=frags,
                               message=f"Valid merge! '{display}' is correct.")
        if candidate in self._prefixes:
            if any(norm.startswith(candidate)
                   for norm in self._display if norm not in found_norms):
                return MergeResult(MergeStatus.PARTIAL, phrase=candidate,
                                   display_phrase=display,
                                   message=f"'{display}' begins a valid merge — keep adding strands!")
            return MergeResult(MergeStatus.INVALID, phrase=candidate, display_phrase=display,
                               message=f"'{display}' only extends merges you have already found.")
        return MergeResult(MergeStatus.INVALID, phrase=candidate, display_phrase=display,
                           message=f"No valid merge forms '{display}'.")