"""Core logic for the Strands word-segmentation puzzle."""


def _key(text):
    """Normalise text for matching: lowercase with all whitespace removed."""
    return "".join(text.lower().split())


class StrandsGame:
    """Strand fragments must be merged into the puzzle's target words/phrases."""

    def __init__(self, theme, targets, strands):
        self.theme = theme
        self._targets = list(targets)
        self._display = {_key(t): t for t in targets}
        self._start = list(strands)
        self.reset()

    def reset(self):
        self._pool = list(self._start)
        self._solved = set()
        self.attempts = 0

    @property
    def target_count(self):
        return len(self._targets)

    def try_merge(self, indices):
        """Merge 1-based numbered strands; returns (success, feedback)."""
        if not indices:
            return False, "No strands selected."
        if len(set(indices)) != len(indices):
            return False, "You cannot use the same strand twice in one merge."
        picked = []
        for i in indices:
            if not 1 <= i <= len(self._pool):
                return False, f"No strand numbered {i}."
            picked.append(self._pool[i - 1])
        self.attempts += 1
        merged = "".join(picked)
        k = _key(merged)
        if k in self._solved:
            return False, f"'{self._display[k]}' is already solved."
        if k in self._display:
            for i in sorted(indices, reverse=True):
                self._pool.pop(i - 1)
            self._solved.add(k)
            left = self.target_count - len(self._solved)
            msg = (f"VALID MERGE! '{self._display[k]}' formed from "
                   f"{len(indices)} strands.")
            msg += f" {left} answer(s) to go." if left else " That was the last one!"
            return True, msg
        return False, f"'{merged}' is not a valid merge. Keep trying!"

    def is_complete(self):
        return len(self._solved) == self.target_count

    def hint(self):
        if self.is_complete():
            return "Puzzle already complete - no hints needed."
        for t in self._targets:
            k = _key(t)
            if k in self._solved:
                continue
            for s in sorted(self._pool, key=len, reverse=True):
                sk = _key(s)
                if sk and k.startswith(sk):
                    return (f"Hint: strand '{s}' begins one remaining answer "
                            f"({len(k)} letters).")
            return f"Hint: a remaining answer is {len(k)} letters long."
        return "No hints available."

    def status(self):
        lines = [f"Theme: {self.theme} | Solved {len(self._solved)}/"
                 f"{self.target_count} | Attempts: {self.attempts}"]
        lines.append("Strands available:")
        for n, s in enumerate(self._pool, 1):
            lines.append(f"  {n:2}. {s}")
        done = ", ".join(self._display[k] for k in sorted(self._solved))
        lines.append(f"Solved: {done or '(none yet)'}")
        return "\n".join(lines)


PUZZLES = [
    {
        "theme": "In the Kitchen",
        "targets": ["spatula", "colander", "whisk", "cutting board", "rolling pin"],
        "strands": ["tu", "bo", "wh", "roll", "der", "cut", "la", "isk",
                    "an", "ting", "p", "spa", "in", "ard", "col", "ing"],
    },
    {
        "theme": "Night Sky",
        "targets": ["meteor", "galaxy", "nebula", "comet"],
        "strands": ["te", "ax", "neb", "met", "or", "gal", "co", "u", "la", "y", "me"],
    },
]