import random


class Game:
    def __init__(self, groups, max_mistakes=4):
        self.groups = groups          # [(name, level, [w1..w4]), ...]
        self.max_mistakes = max_mistakes
        self.mistakes = 0
        self.solved = []              # [(name, level, [words]), ...]
        self.board = [w for _, _, ws in groups for w in ws]
        random.shuffle(self.board)    # mix categories across the 4x4 grid
        self.selected = set()
        self.status = ("", None)

    def shuffle(self):
        random.shuffle(self.board)

    def guess(self):
        words = self.selected
        done = {n for n, _, _ in self.solved}
        counts = {name: sum(w in words for w in ws)
                  for name, _, ws in self.groups if name not in done}
        best = max(counts.values(), default=0)
        if best == 4:
            name = next(n for n, c in counts.items() if c == 4)
            level = next(l for n, l, _ in self.groups if n == name)
            ws = sorted(next(ws for n, _, ws in self.groups if n == name))
            self.solved.append((name, level, ws))
            self.board = [w for w in self.board if w not in words]
            self.selected.clear()
            self.status = ("correct", name)
        else:
            self.mistakes += 1
            self.status = ("one_away", None) if best == 3 else ("wrong", None)

    @property
    def won(self):
        return len(self.solved) == len(self.groups)

    @property
    def over(self):
        return self.won or self.mistakes >= self.max_mistakes