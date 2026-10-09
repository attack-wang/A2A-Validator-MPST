"""Strands engine: merge letter strands into valid words or phrases."""


class Strand:
    __slots__ = ("text", "used")

    def __init__(self, text):
        self.text = text
        self.used = False


class Puzzle:
    def __init__(self, theme, strands, answers):
        self.theme = theme
        self.strands = [Strand(s) for s in strands]
        self.answers = [a.upper() for a in answers]
        self._canon = {a.replace(" ", ""): a for a in self.answers}
        self.found = []

    def available(self):
        return [i for i, s in enumerate(self.strands) if not s.used]

    def merge(self, indices):
        if not indices:
            return False, "No strands selected."
        seen = set()
        for i in indices:
            if not 0 <= i < len(self.strands):
                return False, "Strand %d does not exist." % (i + 1)
            if i in seen:
                return False, "Strand %d picked twice in one merge." % (i + 1)
            seen.add(i)
            if self.strands[i].used:
                return False, "Strand %d ('%s') is already merged." % (i + 1, self.strands[i].text)
        word = "".join(self.strands[i].text for i in indices).upper()
        if word not in self._canon:
            return False, "'%s' is not a valid merge. Keep weaving!" % word
        if self._canon[word] in self.found:
            return False, "'%s' was already found." % self._canon[word]
        for i in indices:
            self.strands[i].used = True
        answer = self._canon[word]
        self.found.append(answer)
        parts = " + ".join(self.strands[i].text for i in indices)
        msg = "Valid merge! %s -> %s" % (parts, answer)
        if self.is_complete():
            msg += "\nAll strands merged. Puzzle complete!"
        else:
            msg += "  (%d/%d found)" % (len(self.found), len(self.answers))
        return True, msg

    def is_complete(self):
        return len(self.found) == len(self.answers)

    def hint(self):
        left = [a for a in self.answers if a not in self.found]
        if not left:
            return "Nothing left to find!"
        return "Hint - remaining words begin with: " + ", ".join(a[:3] + "..." for a in left)


PUZZLES = [
    Puzzle("Compound Words",
           ["BUT", "TER", "FLY", "RAIN", "BOW", "SUN", "SHINE", "NOTE", "BOOK"],
           ["BUTTERFLY", "RAINBOW", "SUNSHINE", "NOTEBOOK"]),
    Puzzle("Everyday Phrases",
           ["BREAK", "A", "LEG", "PIECE", "OF", "CAKE", "ONCE", "UPON", "A", "TIME"],
           ["BREAK A LEG", "PIECE OF CAKE", "ONCE UPON A TIME"]),
    Puzzle("Tech Terms",
           ["KEY", "BOARD", "SOFT", "WARE", "NET", "WORK", "DATA", "BASE"],
           ["KEYBOARD", "SOFTWARE", "NETWORK", "DATABASE"]),
]