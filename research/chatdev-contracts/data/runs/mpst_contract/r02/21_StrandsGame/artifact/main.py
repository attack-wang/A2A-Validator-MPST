#!/usr/bin/env python3
"""Strands: a word-segmentation puzzle. Merge numbered strands to form words or phrases."""

PUZZLES = [
    {
        "name": "Garden Bloom",
        "strands": ["BU", "TTER", "FLY", "SUN", "FLOW", "ER", "BEE", "HIVE"],
        "targets": ["BUTTERFLY", "SUNFLOWER", "BEEHIVE"],
    },
    {
        "name": "Kitchen Mix",
        "strands": ["TOA", "ST", "PAN", "CAKE", "KNI", "FE", "SPA", "TULA"],
        "targets": ["TOAST", "PANCAKE", "KNIFE", "SPATULA"],
    },
    {
        "name": "Space Walk",
        "strands": ["ROC", "KET", "PLA", "NET", "GAL", "AXY", "STA", "R"],
        "targets": ["ROCKET", "PLANET", "GALAXY", "STAR"],
    },
    {
        "name": "Phrase Craft",
        "strands": ["GOOD ", "MORN", "ING", "BIG ", "DATA", "OPEN ", "SESA", "ME"],
        "targets": ["GOOD MORNING", "BIG DATA", "OPEN SESAME"],
    },
]

HELP = """Commands:
  <numbers>   merge strands in the given order, e.g. '1 3 2'
  board       show the current strands and progress
  hint        reveal one valid merge for a remaining target
  restart     reset the current puzzle
  help        show this help
  quit        exit the game"""


class StrandsGame:
    def __init__(self, puzzle):
        self.name = puzzle["name"]
        self.strands = list(puzzle["strands"])
        self.targets = list(puzzle["targets"])
        self.used = [False] * len(self.strands)
        self.found = []
        self.attempts = 0

    def merge(self, picks):
        """Verify a strand formation; return (ok, feedback message)."""
        for n in picks:
            if not 1 <= n <= len(self.strands):
                return False, "Strand %d is out of range (1-%d)." % (n, len(self.strands))
        for n in picks:
            if self.used[n - 1]:
                return False, "Strand %d ('%s') is already merged." % (n, self.strands[n - 1])
        word = "".join(self.strands[n - 1] for n in picks)
        self.attempts += 1
        if word in self.found:
            return False, "'%s' was already found." % word
        if word not in self.targets:
            return False, "X '%s' is not a valid formation. Keep merging!" % word
        for n in picks:
            self.used[n - 1] = True
        self.found.append(word)
        return True, "OK Valid merge! '%s' formed from strands %s." % (
            word, ", ".join(map(str, picks)))

    def complete(self):
        return len(self.found) == len(self.targets)

    def board(self):
        rows = ["Strands for '%s':" % self.name]
        for n, s in enumerate(self.strands, 1):
            rows.append("  %2d. '%s'%s" % (n, s, "   [merged]" if self.used[n - 1] else ""))
        rows.append("Found (%d/%d): %s" % (
            len(self.found), len(self.targets), ", ".join(self.found) or "none yet"))
        return "\n".join(rows)

    def _decompose(self, target, pos=0, path=None):
        path = path if path is not None else []
        if pos == len(target):
            return path
        for n, s in enumerate(self.strands, 1):
            if self.used[n - 1] or target[pos:pos + len(s)] != s:
                continue
            hit = self._decompose(target, pos + len(s), path + [n])
            if hit is not None:
                return hit
        return None

    def hint(self):
        for t in self.targets:
            if t not in self.found:
                picks = self._decompose(t)
                if picks:
                    return "Hint: try merging strands %s." % ", ".join(map(str, picks))
        return "No hint available for the remaining targets."


def play(puzzle):
    game = StrandsGame(puzzle)
    print("\n=== %s ===" % game.name)
    print(game.board())
    print("Merge strands to form %d words/phrases. Type 'help' for commands." % len(game.targets))
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return False
        if not raw:
            continue
        cmd = raw.lower()
        if cmd in ("quit", "exit"):
            return False
        if cmd == "help":
            print(HELP)
        elif cmd == "board":
            print(game.board())
        elif cmd == "hint":
            print(game.hint())
        elif cmd == "restart":
            game = StrandsGame(puzzle)
            print("Puzzle reset.")
            print(game.board())
        else:
            try:
                picks = [int(t) for t in raw.replace(",", " ").split()]
            except ValueError:
                print("Enter strand numbers like '1 3 2', or a command ('help').")
                continue
            if not picks:
                continue
            ok, msg = game.merge(picks)
            print(msg)
            if ok:
                print(game.board())
                if game.complete():
                    print("*** Puzzle complete! All %d strands merged in %d attempts. ***"
                          % (len(game.strands), game.attempts))
                    return True


def main():
    print("Welcome to STRANDS - the word-segmentation puzzle!")
    print("Combine numbered strands into meaningful words or phrases.")
    for puzzle in PUZZLES:
        if not play(puzzle):
            break
        again = input("Next puzzle? [Y/n] > ").strip().lower()
        if again in ("n", "no"):
            break
    print("Thanks for playing Strands. Goodbye!")


if __name__ == "__main__":
    main()