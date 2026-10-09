"""Core Strands puzzle logic: strands, merges, verification, feedback."""


class StrandsPuzzle:
    def __init__(self, theme, strands, solutions, spangram=None):
        self.theme = theme
        self.strands = list(strands)
        self.solutions = list(solutions)
        self.spangram = spangram
        self.found = set()

    def merge(self, tokens):
        """Merge strands by 1-based numbers. Returns (word, feedback)."""
        try:
            idxs = [int(t) - 1 for t in tokens]
        except ValueError:
            return None, "Invalid input. Use strand numbers, e.g. '1 4'."
        if not idxs:
            return None, "Select at least one strand."
        if any(i < 0 or i >= len(self.strands) for i in idxs):
            return None, "Strand number out of range."
        if len(set(idxs)) != len(idxs):
            return None, "Duplicate strand in selection."
        word = "".join(self.strands[i] for i in idxs)
        if word in self.solutions:
            if word in self.found:
                return word, f"'{word}' was already found."
            self.found.add(word)
            tag = " Spangram!" if word == self.spangram else ""
            left = len(self.solutions) - len(self.found)
            return word, f"Valid merge: '{word}' accepted!{tag} {left} to go."
        return word, f"'{word}' is not a valid formation."

    def spell(self, word):
        """Return 0-based strand indices spelling word, or None."""
        idxs, pos, used = [], 0, set()
        while pos < len(word):
            for i, s in enumerate(self.strands):
                if i not in used and word.startswith(s, pos):
                    idxs.append(i)
                    used.add(i)
                    pos += len(s)
                    break
            else:
                return None
        return idxs

    def hint(self):
        left = [w for w in self.solutions if w not in self.found]
        if not left:
            return "Puzzle already complete -- no hints needed."
        idxs = self.spell(left[0])
        if idxs:
            nums = " ".join(str(i + 1) for i in idxs)
            return f"Hint: strands {nums} merge into a solution."
        return f"Hint: a remaining word has {len(left[0])} letters."

    def is_complete(self):
        return set(self.solutions) <= self.found

    def display(self):
        rows = [
            f"Theme: {self.theme}",
            f"Found {len(self.found)}/{len(self.solutions)} words.",
        ]
        for i, s in enumerate(self.strands, 1):
            rows.append(f"  [{i:>2}] {s}")
        if self.found:
            rows.append("Found: " + ", ".join(sorted(self.found)))
        return "\n".join(rows)


PUZZLES = [
    StrandsPuzzle(
        "Compound Nature",
        ["sun", "flower", "rain", "bow", "book", "worm", "star", "fish"],
        ["sunflower", "rainbow", "bookworm", "starfish"],
        spangram="rainbow",
    ),
    StrandsPuzzle(
        "On the Menu",
        ["pan", "cake", "sand", "wich", "noo", "dles", "to", "mato"],
        ["pancake", "sandwich", "noodles", "tomato"],
        spangram="sandwich",
    ),
]