'''
puzzle.py
Game engine for the Strands word-segmentation puzzle.
The Puzzle class:
    * builds a shuffled board of Strand fragments from a puzzle spec,
    * validates merge attempts (exact strand order, spelling, bonuses),
    * commits successful merges and awards points,
    * provides progressive hints,
    * reports completion once every target word has been merged.
'''
import random
from typing import Dict, List, Optional, Tuple
from models import MergeResult, Strand
from dictionary import WordDictionary
POINTS_CORE = 250      # points for merging the core (spangram-like) word
POINTS_VALID = 100     # points for merging a normal target word
POINTS_BONUS = 10      # points for a dictionary-valid bonus merge
HINT_COST = 25         # score penalty per hint
class Puzzle:
    """State and rules for one round of Strands."""
    def __init__(self, spec: dict, dictionary: WordDictionary) -> None:
        """Create a puzzle from a spec dict and a bonus-word dictionary."""
        self.name = spec["name"]
        self.theme = spec["theme"]
        self.difficulty = spec.get("difficulty", "Medium")
        self.description = spec.get("description", "")
        self.dictionary = dictionary
        self.words: List[str] = list(spec["words"].keys())
        self.core_word = spec.get("core_word") or self._longest_word()
        self.splits: Dict[str, List[str]] = {w: list(s) for w, s in spec["words"].items()}
        # Defensive check: every split list must rebuild its word exactly.
        for word, parts in self.splits.items():
            if "".join(parts) != word:
                raise ValueError(f"Puzzle '{self.name}': strands for '{word}' do not rebuild the word.")
        self.hint_level: Dict[str, int] = {w: 0 for w in self.words}  # required by get_hint
        self.score: int = 0
        self.strands: List[Strand] = []
        self.word_strand_ids: Dict[str, List[str]] = {}
        self.found: Dict[str, int] = {}   # word -> points awarded
        self.bonus_words: List[str] = []
        self._build_strands()
        self.shuffled: List[Strand] = []
        self.shuffle()
    # ------------------------------------------------------------------ setup
    def _longest_word(self) -> str:
        """Fallback core word: the longest target word."""
        return max(self.words, key=len)
    def _build_strands(self) -> None:
        """Create one Strand per fragment occurrence with unique IDs.
        IDs are unique per occurrence (S1, S2, ...) so duplicate fragment
        texts across words remain distinguishable on the board.
        """
        counter = 0
        for word in self.words:
            ids: List[str] = []
            for fragment in self.splits[word]:
                counter += 1
                sid = f"S{counter}"
                self.strands.append(Strand(id=sid, text=fragment.upper()))
                ids.append(sid)
            self.word_strand_ids[word] = ids
    def shuffle(self) -> None:
        """Randomize board order; only unused strands are ever shown."""
        self.shuffled = [s for s in self.strands if not s.used]
        random.shuffle(self.shuffled)
    # ------------------------------------------------------------- inspection
    def strand_by_id(self, sid: str) -> Optional[Strand]:
        """Return the Strand with the given id, or None if not found."""
        return next((s for s in self.strands if s.id == sid), None)
    def is_complete(self) -> bool:
        """True when every target word has been merged (all strands consumed)."""
        return len(self.found) == len(self.words)
    def display_strands(self) -> None:
        """Print every unused strand as 'ID: TEXT' in shuffled board order."""
        print("\n--- Strands on the board ---")
        for strand in self.shuffled:
            if not strand.used:
                print(f"  {strand.id}: {strand.text}")
        print("----------------------------")
    # ------------------------------------------------------------- validation
    def validate_merge(self, selection: List[str]) -> MergeResult:
        """Validate an ordered list of strand ids as a potential merge."""
        # selection: list of strand ids in order
        if len(selection) < 2:
            return MergeResult("too_few", message="Select at least two strands to form a merge.")
        ids_seen = set()
        for sid in selection:
            strand = self.strand_by_id(sid)
            if strand is None:
                return MergeResult("unknown_strand", message=f"Strand '{sid}' does not exist.")
            if strand.used:
                return MergeResult("used_strand", message=f"Strand '{sid}' was already merged.")
            if sid in ids_seen:
                return MergeResult("duplicate", message=f"Strand '{sid}' is selected more than once.")
            ids_seen.add(sid)
        candidate = "".join(self.strand_by_id(s).text for s in selection)
        # exact target match: right word AND right strands, in order
        for word in self.words:
            if word in self.found:
                continue
            if selection == self.word_strand_ids[word]:
                pts = POINTS_CORE if word == self.core_word else POINTS_VALID
                status = "core" if word == self.core_word else "valid"
                return MergeResult(status, word=word, points=pts,
                                   message=f"✔ Valid merge: '{word}' (+{pts} pts)")
        # right word, wrong strands
        if candidate in self.words:
            if candidate in self.found:
                return MergeResult("already_found", word=candidate,
                                   message=f"'{candidate}' is already merged.")
            return MergeResult("wrong_strands", word=candidate,
                               message=f"Spelling matches '{candidate}', but those strands belong to other words.")
        # bonus word: real word, but not one of the targets
        if self.dictionary.is_valid(candidate):
            return MergeResult("bonus", word=candidate, points=POINTS_BONUS,
                               message=f"✨ Bonus word: '{candidate}' (+{POINTS_BONUS} pts)")
        return MergeResult("invalid", word=candidate,
                           message=f"'{candidate}' is not a valid merge.")
    def commit_merge(self, result: MergeResult) -> None:
        """Apply a validated merge result to the puzzle state."""
        if result.status in ("valid", "core"):
            for sid in self.word_strand_ids[result.word]:
                self.strand_by_id(sid).used = True
            self.found[result.word] = result.points
            self.shuffle()  # refresh the board view
        elif result.status == "bonus":
            self.bonus_words.append(result.word)
    # ------------------------------------------------------------------ hints
    def get_hint(self) -> Tuple[str, int]:
        """Return the next progressive hint for the cheapest unfound word."""
        unfound = [w for w in self.words if w not in self.found]
        if not unfound:
            return ("Puzzle already complete!", 0)
        # pick the word with the lowest hint level
        word = min(unfound, key=lambda w: self.hint_level.get(w, 0))
        level = self.hint_level.get(word, 0)
        self.hint_level[word] = level + 1
        cost = HINT_COST
        if level == 0:
            ids = self.word_strand_ids[word]
            lens = "+".join(str(len(self.strand_by_id(i).text)) for i in ids)
            return (f"Hint: one unfound word uses {len(ids)} strands of sizes {lens}.", cost)
        if level == 1:
            first = self.strand_by_id(self.word_strand_ids[word][0]).text
            return (f"Hint: that word starts with the strand '{first}'.", cost)
        return (f"Hint: the word is '{word}'.", cost)