"""Strands - a word-segmentation puzzle.

Combine numbered strands of text into meaningful words or phrases.
Each valid merge is confirmed with feedback; the puzzle is complete
when every strand has been merged into a target word exactly once.
"""

PUZZLES = [
    {
        "name": "Warm-Up",
        "strands": ["CAT", "ER", "PIL", "LOW", "AR", "ROW"],
        "targets": [("CATER", (0, 1)), ("PILLOW", (2, 3)), ("ARROW", (4, 5))],
    },
    {
        "name": "Nature Walk",
        "strands": ["BUT", "TER", "FLY", "SUN", "FLOW", "ER"],
        "targets": [("BUTTERFLY", (0, 1, 2)), ("SUNFLOWER", (3, 4, 5))],
    },
    {
        "name": "Night Sky",
        "strands": ["MOON", "LIGHT", "STAR", "FISH", "RAIN", "BOW"],
        "targets": [("MOONLIGHT", (0, 1)), ("STARFISH", (2, 3)), ("RAINBOW", (4, 5))],
    },
    {
        "name": "Everyday Phrases",
        "strands": ["GOOD ", "MORN", "ING", "NOTE", "BOOK"],
        "targets": [("GOOD MORNING", (0, 1, 2)), ("NOTEBOOK", (3, 4))],
    },
]


def validate(puzzle):
    """Ensure every strand is used exactly once and targets match their strands."""
    strands, seen = puzzle["strands"], []
    for word, idx in puzzle["targets"]:
        assert "".join(strands[i] for i in idx) == word, "target/strand mismatch: " + word
        seen.extend(idx)
    assert sorted(seen) == list(range(len(strands))), "each strand must be used exactly once"


class StrandsGame:
    def __init__(self, puzzles=PUZZLES):
        for p in puzzles:
            validate(p)
        self.puzzles = puzzles

    def play(self):
        print("=" * 46)
        print(" STRANDS - merge the strands to form words!")
        print(" Commands: strand numbers (e.g. '1 3 2'),")
        print("           'h' = hint, 'q' = quit")
        print("=" * 46 + "\n")
        for level, puzzle in enumerate(self.puzzles, 1):
            if not self.play_puzzle(level, puzzle):
                print("Thanks for playing Strands. Goodbye!")
                return
        print("*" * 46)
        print(" Incredible! You solved every Strands puzzle!")
        print("*" * 46)

    def play_puzzle(self, level, puzzle):
        strands = puzzle["strands"]
        remaining = {word: set(idx) for word, idx in puzzle["targets"]}
        used, found = set(), []
        print(f"--- Level {level}: {puzzle['name']} "
              f"({len(remaining)} words hidden in {len(strands)} strands) ---")
        while remaining:
            self.show(strands, used, found)
            try:
                choice = input("Merge strands> ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                return False
            if choice in ("q", "quit", "exit"):
                return False
            if choice in ("h", "hint"):
                self.hint(strands, remaining)
                continue
            idx = self.parse(choice, len(strands))
            if idx is None:
                print("Enter strand numbers separated by spaces (e.g. '2 4 1').\n")
                continue
            if len(set(idx)) != len(idx):
                print("Each strand can only be used once per merge.\n")
                continue
            if any(i in used for i in idx):
                print("One or more of those strands are already merged.\n")
                continue
            word = "".join(strands[i] for i in idx)
            match = next((w for w, s in remaining.items() if s == set(idx)), None)
            if match is not None and word == match:
                remaining.pop(match)
                used |= set(idx)
                found.append(match)
                msg = f"VALID MERGE! '{match}' is locked in."
                if remaining:
                    msg += f" {len(remaining)} word(s) to go."
                print(msg + "\n")
            elif match is not None:
                print("Right strands, wrong order! Rearrange them to spell the word.\n")
            elif any(w.startswith(word) for w in remaining):
                print(f"'{word.strip()}' is a promising start - keep extending it!\n")
            else:
                print(f"'{word.strip()}' is not a valid merge. Try another combination.\n")
        print("PUZZLE COMPLETE! You formed: " + ", ".join(found) + "\n")
        return True

    @staticmethod
    def show(strands, used, found):
        print("\nStrands:")
        for i, s in enumerate(strands):
            state = "  <- merged" if i in used else ""
            print(f"  [{i + 1}] '{s}'{state}")
        if found:
            print("Found: " + ", ".join(found))

    @staticmethod
    def hint(strands, remaining):
        word, need = next(iter(remaining.items()))
        i = min(need)
        print(f"Hint: strand [{i + 1}] '{strands[i]}' begins a word still hidden "
              f"({len(word)} letters long).\n")

    @staticmethod
    def parse(text, n):
        try:
            idx = [int(t) - 1 for t in text.replace(",", " ").split()]
        except ValueError:
            return None
        if not idx or any(i < 0 or i >= n for i in idx):
            return None
        return tuple(idx)


def main():
    StrandsGame().play()


if __name__ == "__main__":
    main()