'''
game_engine.py
Core game logic for Strands: state tracking, merge verification,
hints, undo, and completion detection.
'''
from feedback import Feedback, FeedbackType, is_common_word
from puzzle import Puzzle
class StrandsGame:
    """Drives one or more puzzles: validates merges and tracks progress."""
    def __init__(self, puzzles):
        """Store the puzzle list and load the first puzzle."""
        if not puzzles:
            raise ValueError("StrandsGame needs at least one puzzle")
        self.puzzles = puzzles
        self.current_index = 0
        self.stats = {"words_formed": 0, "invalid_attempts": 0,
                      "hints_used": 0, "puzzles_solved": 0}
        self._load_puzzle(0)
    def _load_puzzle(self, index):
        """(Re)initialize per-puzzle state for puzzles[index]."""
        self.puzzle = self.puzzles[index]
        self.used_strands = set()
        self.merged_words = []      # list of (word, tuple(indices))
        self.move_history = []      # list of (word, indices) for undo
        self.hints_used_this_puzzle = 0
        self.solved = False
    @property
    def remaining_strands(self):
        """Return the list of strand indices not yet consumed."""
        return [i for i in range(len(self.puzzle.strands)) if i not in self.used_strands]
    def merged_text(self, indices):
        """Concatenate the strands at `indices` in the given order."""
        return "".join(self.puzzle.strands[i] for i in indices)
    def attempt_merge(self, indices):
        """Validate a strand selection and, if it spells a target word, lock it in."""
        # --- structural validation -------------------------------------
        if len(indices) < 2:
            return Feedback(FeedbackType.WARNING,
                            "Select at least 2 strands to form a word.",
                            "e.g. `merge 1 3`")
        for i in indices:
            if not isinstance(i, int) or not 0 <= i < len(self.puzzle.strands):
                return Feedback(FeedbackType.WARNING,
                                f"Strand number {i} is out of range 1-{len(self.puzzle.strands)}.")
        if len(set(indices)) != len(indices):
            return Feedback(FeedbackType.WARNING, "You picked the same strand twice.")
        for i in indices:
            if i in self.used_strands:
                return Feedback(FeedbackType.WARNING,
                                f"Strand {i + 1} is already used by a formed word.")
        word = self.merged_text(indices)
        target = self.puzzle.word_for_strands(indices)
        if target is None:
            self.stats["invalid_attempts"] += 1
            if is_common_word(word):
                return Feedback(FeedbackType.NEAR_MISS,
                                f"{word!r} is a real word, but it is not part of this puzzle.",
                                f"Theme: {self.puzzle.theme}")
            return Feedback(FeedbackType.ERROR,
                            f"{word!r} is not a valid word.",
                            "Try combining strands in a different order.")
        # --- success ----------------------------------------------------
        ftype = FeedbackType.KEY_WORD if self.puzzle.is_key_word(target) else FeedbackType.SUCCESS
        for i in indices:
            self.used_strands.add(i)
        self.merged_words.append((target, tuple(indices)))
        self.move_history.append((target, tuple(indices)))
        self.stats["words_formed"] += 1
        detail = f"{len(indices)} strands merged"
        if ftype is FeedbackType.KEY_WORD:
            detail = "KEY WORD found!"
        self.check_completion()
        return Feedback(ftype, f"You formed {target}!", detail)
    def undo(self):
        """Undo the most recent successful merge, freeing its strands."""
        if not self.move_history:
            return Feedback(FeedbackType.INFO, "Nothing to undo.")
        word, indices = self.move_history.pop()
        for i in indices:
            self.used_strands.discard(i)
        # remove from merged_words as well (last occurrence)
        for k in range(len(self.merged_words) - 1, -1, -1):
            if self.merged_words[k][0] == word and self.merged_words[k][1] == tuple(indices):
                self.merged_words.pop(k)
                break
        self.solved = False
        return Feedback(FeedbackType.INFO, f"Undid {word}; strands returned to the board.")
    def request_hint(self):
        """Reveal a nudge about the first word not yet formed."""
        formed = {w for w, _ in self.merged_words}
        remaining = [w for w in self.puzzle.word_list if w not in formed]
        if not remaining:
            return Feedback(FeedbackType.INFO, "No hints needed — every word is formed!")
        target = remaining[0]
        idxs = self.puzzle.strands_for_word(target)
        self.hints_used_this_puzzle += 1
        self.stats["hints_used"] += 1
        first_strand = self.puzzle.strands[idxs[0]]
        return Feedback(FeedbackType.HINT,
                        f"A {len(idxs)}-strand word starts with strand {idxs[0] + 1} ({first_strand!r}).",
                        f"{len(remaining)} word(s) still hidden.")
    def reset_puzzle(self):
        """Clear all progress on the current puzzle."""
        self._load_puzzle(self.current_index)
        return Feedback(FeedbackType.INFO, "Puzzle reset. Fresh strands, fresh start!")
    def next_puzzle(self):
        """Advance to the next puzzle if the current one is solved."""
        if not self.solved:
            return Feedback(FeedbackType.WARNING,
                            "Finish (or `reset`) the current puzzle before moving on.")
        if self.current_index + 1 >= len(self.puzzles):
            return Feedback(FeedbackType.VICTORY,
                            "That was the last puzzle — you cleared Strands!")
        self.current_index += 1
        self._load_puzzle(self.current_index)
        return Feedback(FeedbackType.INFO,
                        f"Puzzle {self.current_index + 1}/{len(self.puzzles)}: {self.puzzle.title}")
    def check_completion(self):
        """Mark the puzzle solved when every strand has been consumed."""
        if not self.solved and len(self.used_strands) == len(self.puzzle.strands):
            self.solved = True
            self.stats["puzzles_solved"] += 1
        return self.solved