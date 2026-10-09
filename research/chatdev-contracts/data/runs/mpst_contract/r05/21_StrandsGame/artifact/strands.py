"""Core engine for 'Strands', a word-segmentation puzzle."""

import random


def _norm(text):
    return text.replace(" ", "")


class Strand:
    """One mergeable piece of text shown on the board."""

    __slots__ = ("sid", "text")

    def __init__(self, sid, text):
        self.sid = sid
        self.text = text

    def __str__(self):
        return f"{self.sid}:{self.text}"


class StrandsPuzzle:
    """A board of strands that must be merged into target words/phrases."""

    def __init__(self, name, theme, entries):
        self.name = name
        self.theme = theme
        self.entries = []  # (display, target, pieces)
        for answer, pieces in entries:
            display = answer.upper()
            target = _norm(display)
            parts = [p.upper() for p in pieces]
            if "".join(parts) != target:
                raise ValueError(f"Strands {parts} do not spell '{answer}'.")
            self.entries.append((display, target, parts))
        self.spangram = max(self.entries, key=lambda e: len(e[1]))[1]
        self.found = []
        self.reset()

    def reset(self):
        """Rebuild and shuffle the strand pool (found progress is kept)."""
        self.pool = []
        sid = 1
        for display, _, pieces in self.entries:
            if display in self.found:
                continue
            for piece in pieces:
                self.pool.append(Strand(sid, piece))
                sid += 1
        random.shuffle(self.pool)

    def is_complete(self):
        return len(self.found) == len(self.entries)

    def _answer_for(self, pieces):
        joined = "".join(pieces)
        matches = [(d, t) for d, t, _ in self.entries if t == joined]
        for display, _ in matches:
            if display not in self.found:
                return display
        return matches[0][0] if matches else None

    def merge(self, sids):
        """Attempt to merge strands by id. Returns (success, message)."""
        lookup = {s.sid: s for s in self.pool}
        unknown = [i for i in sids if i not in lookup]
        if unknown:
            return False, f"No strand(s) {unknown} on the board."
        if len(set(sids)) != len(sids):
            return False, "A strand can only be used once per merge."
        strands = [lookup[i] for i in sids]
        pieces = [s.text for s in strands]
        joined = "".join(pieces)
        answer = self._answer_for(pieces)
        if answer is None:
            near = [
                d for d, t, _ in self.entries
                if d not in self.found and t.startswith(joined)
                and len(joined) < len(t)
            ]
            if near:
                return False, (f"'{joined}' is on the right track, "
                               f"but it is not a full word yet.")
            return False, f"'{joined}' is not a valid merge. Strands remain."
        if answer in self.found:
            return False, f"'{answer}' has already been found."
        self.found.append(answer)
        for strand in strands:
            self.pool.remove(strand)
        for idx, strand in enumerate(self.pool, 1):
            strand.sid = idx
        if _norm(answer) == self.spangram:
            return True, f"SPANGRAM! '{answer}' spans the whole theme!"
        return True, f"Valid merge: {' + '.join(pieces)} = '{answer}'"