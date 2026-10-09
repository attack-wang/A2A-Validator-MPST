import random
import sys

SIZE = 4


def read_key():
    """Return 'UP'/'DOWN'/'LEFT'/'RIGHT'/'QUIT', or None for ignored keys."""
    try:
        import msvcrt
        key = msvcrt.getwch()
        if key in ('\x00', '\xe0'):
            key = msvcrt.getwch()
        return {'H': 'UP', 'P': 'DOWN', 'K': 'LEFT', 'M': 'RIGHT',
                'q': 'QUIT', 'Q': 'QUIT'}.get(key)
    except ImportError:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                seq = sys.stdin.read(2)
                return {'[A': 'UP', '[B': 'DOWN',
                        '[C': 'RIGHT', '[D': 'LEFT'}.get(seq)
            return 'QUIT' if ch in ('q', 'Q') else None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


class Game2048:
    def __init__(self):
        self.grid = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.best = 0
        self.spawn()
        self.spawn()

    def spawn(self):
        empty = [(r, c) for r in range(SIZE) for c in range(SIZE)
                 if self.grid[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            self.grid[r][c] = 2 if random.random() < 0.9 else 4

    @staticmethod
    def slide(row):
        tiles = [v for v in row if v]
        out, gained, i = [], 0, 0
        while i < len(tiles):
            if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                value = tiles[i] * 2
                out.append(value)
                gained += value
                i += 2
            else:
                out.append(tiles[i])
                i += 1
        return out + [0] * (SIZE - len(out)), gained

    def move(self, direction):
        grid = self.grid
        if direction in ('LEFT', 'RIGHT'):
            lines = [list(row) for row in grid]
            rev = direction == 'RIGHT'
        else:
            lines = [list(col) for col in zip(*grid)]
            rev = direction == 'DOWN'
        if rev:
            lines = [line[::-1] for line in lines]
        new_lines, gained = [], 0
        for line in lines:
            slid, s = self.slide(line)
            new_lines.append(slid[::-1] if rev else slid)
            gained += s
        if direction in ('LEFT', 'RIGHT'):
            new_grid = new_lines
        else:
            new_grid = [list(row) for row in zip(*new_lines)]
        changed = new_grid != grid
        if changed:
            self.grid = new_grid
            self.score += gained
            self.best = max(self.best,
                            max(v for row in self.grid for v in row))
        return changed

    def moves_available(self):
        for r in range(SIZE):
            for c in range(SIZE):
                v = self.grid[r][c]
                if v == 0:
                    return True
                if c + 1 < SIZE and self.grid[r][c + 1] == v:
                    return True
                if r + 1 < SIZE and self.grid[r + 1][c] == v:
                    return True
        return False

    def render(self):
        highest = max(v for row in self.grid for v in row)
        print(f"Score: {self.score}    Highest tile: {highest}", flush=True)
        border = '+' + '------+' * SIZE
        print(border, flush=True)
        for row in self.grid:
            cells = '|'.join(f'{v:^5}' if v else '     ' for v in row)
            print('|' + cells + '|', flush=True)
            print(border, flush=True)


def main():
    game = Game2048()
    print("2048 - slide tiles with the arrow keys (q quits).", flush=True)
    game.render()
    while True:
        key = read_key()
        if key == 'QUIT':
            print(f"Quit. Final score: {game.score}, "
                  f"highest tile: {game.best}", flush=True)
            break
        if key is None or not game.move(key):
            continue
        game.spawn()
        game.render()
        if not game.moves_available():
            print(f"Game over! Final score: {game.score}, "
                  f"highest tile: {game.best}", flush=True)
            break


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.", flush=True)