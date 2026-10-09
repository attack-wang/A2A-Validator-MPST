"""Strands: a word-segmentation puzzle. Merge letter strands into words."""

import random

PUZZLES = [
    {"name": "Around the House",
     "strands": ["PIL", "LOW", "CAR", "PET", "BUT", "TER", "FLY",
                 "CAN", "DLE", "MIR", "ROR"],
     "targets": ["PILLOW", "CARPET", "BUTTERFLY", "CANDLE", "MIRROR"]},
    {"name": "Sky and Sea",
     "strands": ["SUN", "FLOW", "ER", "RAIN", "BOW", "THUN", "DER",
                 "MOON", "LIGHT", "STAR", "FISH"],
     "targets": ["SUNFLOWER", "RAINBOW", "THUNDER", "MOONLIGHT", "STARFISH"]},
    {"name": "In the Kitchen",
     "strands": ["TOA", "STER", "BLEN", "DER", "KET", "TLE", "SPA",
                 "GHET", "TI", "PAN", "TRY"],
     "targets": ["TOASTER", "BLENDER", "KETTLE", "SPAGHETTI", "PANTRY"]},
]


class StrandsGame:
    def __init__(self, puzzle):
        self.name = puzzle["name"]
        self.strands = list(puzzle["strands"])
        random.shuffle(self.strands)
        self.targets = list(puzzle["targets"])
        self.used = [False] * len(self.strands)
        self.solved = set()
        self.history = []

    def reset(self):
        self.used = [False] * len(self.strands)
        self.solved = set()
        self.history = []

    def merge(self, idxs):
        if not idxs:
            return "Enter at least one strand number."
        if len(set(idxs)) != len(idxs):
            return "Duplicate strand numbers are not allowed."
        for i in idxs:
            if not 1 <= i <= len(self.strands):
                return f"Strand {i} is out of range (1-{len(self.strands)})."
            if self.used[i - 1]:
                return f"Strand {i} ({self.strands[i - 1]}) is already merged."
        word = "".join(self.strands[i - 1] for i in idxs)
        if word in self.targets:
            if word in self.solved:
                return f"'{word}' was already merged."
            for i in idxs:
                self.used[i - 1] = True
            self.solved.add(word)
            self.history.append((tuple(idxs), word))
            left = len(self.targets) - len(self.solved)
            msg = f"Valid merge! '{word}' formed from {len(idxs)} strand(s)."
            msg += (" All strands merged -- puzzle complete!"
                    if left == 0 else f" {left} word(s) still hidden.")
            return msg
        if any(t.startswith(word) for t in self.targets if t not in self.solved):
            return (f"'{word}' is not a word yet, but it begins one -- "
                    "keep pulling strands!")
        if any(word in t for t in self.targets if t not in self.solved):
            return (f"'{word}' appears inside a hidden word, but hidden words "
                    "start elsewhere.")
        return f"'{word}' is not a valid merge."

    def undo(self):
        if not self.history:
            return "Nothing to undo."
        idxs, word = self.history.pop()
        for i in idxs:
            self.used[i - 1] = False
        self.solved.discard(word)
        return f"Undid merge '{word}'."

    def hint(self):
        left = [t for t in self.targets if t not in self.solved]
        if not left:
            return "Puzzle already complete -- no hints needed!"
        target = random.choice(left)
        avail = [i for i in range(len(self.strands)) if not self.used[i]]

        def dfs(pos, path):
            if pos == len(target):
                return path
            for i in avail:
                if i in path:
                    continue
                s = self.strands[i]
                if target.startswith(s, pos):
                    res = dfs(pos + len(s), path + [i])
                    if res is not None:
                        return res
            return None

        seq = dfs(0, [])
        if seq:
            i = seq[0]
            return (f"Hint: strand {i + 1} ('{self.strands[i]}') "
                    "begins one of the hidden words.")
        return "Hint unavailable."

    def board(self):
        rows = [f"=== STRANDS: {self.name} ===", "Strands:"]
        for i, s in enumerate(self.strands, 1):
            rows.append(f"  {i:2}. {'(merged)' if self.used[i - 1] else s}")
        rows.append("Solved words: " + (", ".join(sorted(self.solved)) or "none yet"))
        rows.append(f"Words remaining: {len(self.targets) - len(self.solved)}")
        return "\n".join(rows)


def choose_puzzle():
    for i, p in enumerate(PUZZLES, 1):
        print(f"  {i}. {p['name']} ({len(p['targets'])} words, "
              f"{len(p['strands'])} strands)")
    while True:
        raw = input(f"Pick a puzzle (1-{len(PUZZLES)}): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(PUZZLES):
            return PUZZLES[int(raw) - 1]
        print("Invalid choice -- enter a listed number.")


def play(puzzle):
    game = StrandsGame(puzzle)
    print(game.board())
    print("Merge strands by number, e.g. '3 7'. "
          "Commands: undo | hint | reset | board | quit")
    while True:
        cmd = input("> ").strip().lower()
        if not cmd:
            continue
        if cmd in ("q", "quit"):
            print("Thanks for playing Strands!")
            return
        if cmd in ("u", "undo"):
            print(game.undo())
        elif cmd == "hint":
            print(game.hint())
        elif cmd == "reset":
            game.reset()
            print("Puzzle reset.")
            print(game.board())
        elif cmd == "board":
            print(game.board())
        else:
            try:
                idxs = [int(t) for t in cmd.replace(",", " ").split()]
            except ValueError:
                print("Enter strand numbers like '1 2', or undo/hint/reset/quit.")
                continue
            print(game.merge(idxs))
            if len(game.solved) == len(game.targets):
                print(game.board())
                print(f"Congratulations! Every strand of '{game.name}' "
                      "is correctly merged.")
                return


def main():
    print("Welcome to STRANDS -- combine letter strands into meaningful words!")
    try:
        while True:
            play(choose_puzzle())
            if input("Play another puzzle? (y/n): ").strip().lower() != "y":
                break
    except (EOFError, KeyboardInterrupt):
        pass
    print("Goodbye!")


if __name__ == "__main__":
    main()