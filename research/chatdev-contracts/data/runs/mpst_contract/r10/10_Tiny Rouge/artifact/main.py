"""Tower of the Sorcerer-inspired roguelike. 80x80 grid, W/A/S/D movement."""
import random
import sys

W = H = 80
VIEW = 23
DIRS = {"w": (0, -1), "a": (-1, 0), "s": (0, 1), "d": (1, 0)}
MONSTER_NAMES = ["Slime", "Bat", "Skeleton", "Goblin", "Ghost", "Dark Wizard"]

try:
    import msvcrt

    def read_key(timeout=0.1):
        return msvcrt.getwch() if msvcrt.kbhit() else None
except ImportError:
    import select
    import termios
    import tty

    def read_key(timeout=0.1):
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            if select.select([sys.stdin], [], [], timeout)[0]:
                return sys.stdin.read(1)
            return None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


class Game:
    def __init__(self):
        self.rng = random.Random()
        self.level = 1
        self.max_hp = 100
        self.hp = self.max_hp
        self.msgs = ["Welcome to the Tower. Reach the door (D)."]
        self.last_monster = None
        self.over = False
        self.build_level()

    def log(self, text):
        self.msgs.append(text)
        self.msgs = self.msgs[-5:]

    def build_level(self):
        rng = self.rng
        g = [["#"] * W for _ in range(H)]
        # Randomized DFS maze on odd cells guarantees a path between all floors.
        g[1][1] = "."
        stack = [(1, 1)]
        while stack:
            x, y = stack[-1]
            opts = []
            for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)):
                nx, ny = x + dx, y + dy
                if 1 <= nx <= W - 2 and 1 <= ny <= H - 2 and g[ny][nx] == "#":
                    opts.append((nx, ny, dx, dy))
            if opts:
                nx, ny, dx, dy = rng.choice(opts)
                g[y + dy // 2][x + dx // 2] = "."
                g[ny][nx] = "."
                stack.append((nx, ny))
            else:
                stack.pop()
        # Braid: open some interior walls (always between two floor cells) for loops.
        for _ in range(500):
            x, y = rng.randrange(1, W - 1), rng.randrange(1, H - 1)
            if g[y][x] == "#" and (x % 2) != (y % 2):
                g[y][x] = "."
        self.grid = g
        self.door = (W - 3, H - 3)  # odd,odd cell -> guaranteed floor & reachable
        self.px, self.py = 1, 1
        self.monsters = []
        self.chests = []
        floors = [(x, y) for y in range(1, H - 1) for x in range(1, W - 1)
                  if g[y][x] == "." and (x, y) not in ((1, 1), self.door)]
        rng.shuffle(floors)
        for _ in range(min(14 + self.level * 2, len(floors))):
            x, y = floors.pop()
            self.monsters.append({
                "x": x, "y": y,
                "name": rng.choice(MONSTER_NAMES),
                "hp": rng.randint(4, 12) + self.level * 2,
                "atk": rng.randint(1, 3) + self.level // 2,
            })
        for _ in range(min(8, len(floors))):
            x, y = floors.pop()
            self.chests.append((x, y))

    def monster_at(self, x, y):
        for m in self.monsters:
            if m["x"] == x and m["y"] == y:
                return m
        return None

    def move(self, dx, dy):
        if self.over:
            return
        nx, ny = self.px + dx, self.py + dy
        if not (0 <= nx < W and 0 <= ny < H) or self.grid[ny][nx] == "#":
            self.log("A wall blocks your way.")
            return
        self.px, self.py = nx, ny
        m = self.monster_at(nx, ny)
        if m:
            self.hp -= m["hp"]
            self.last_monster = dict(m)
            self.monsters.remove(m)
            self.log("Fought %s (HP %d, ATK %d): -%d HP." %
                     (m["name"], m["hp"], m["atk"], m["hp"]))
            if self.hp <= 0:
                self.hp = 0
                self.over = True
                self.log("You died. Press R to restart or Q to quit.")
            return
        if (nx, ny) in self.chests:
            self.chests.remove((nx, ny))
            heal = self.rng.randint(20, 30)
            self.hp = min(self.max_hp, self.hp + heal)
            self.log("Opened a treasure chest: +%d HP." % heal)
            return
        if (nx, ny) == self.door:
            self.level += 1
            self.log("Descended to level %d." % self.level)
            self.build_level()

    def draw(self):
        vx = min(max(self.px - VIEW // 2, 0), W - VIEW)
        vy = min(max(self.py - VIEW // 2, 0), H - VIEW)
        mset = {(m["x"], m["y"]) for m in self.monsters}
        lines = []
        for y in range(vy, vy + VIEW):
            row = []
            for x in range(vx, vx + VIEW):
                if x == self.px and y == self.py:
                    row.append("@")
                elif (x, y) == self.door:
                    row.append("D")
                elif (x, y) in mset:
                    row.append("M")
                elif (x, y) in self.chests:
                    row.append("$")
                else:
                    row.append(self.grid[y][x])
            lines.append("".join(row))
        panel = [
            "TOWER OF THE SORCERER - ROGUELIKE",
            "Level: %d" % self.level,
            "HP: %d/%d" % (self.hp, self.max_hp),
            "Pos: (%d,%d)" % (self.px, self.py),
            "",
        ]
        if self.last_monster:
            m = self.last_monster
            panel.append("Last monster encountered:")
            panel.append("  Name: %s" % m["name"])
            panel.append("  HP: %d  ATK: %d" % (m["hp"], m["atk"]))
        else:
            panel.append("No monster encountered yet.")
        panel += ["", "Monsters left: %d  Chests: %d" % (len(self.monsters), len(self.chests)),
                  "W/A/S/D move | R restart | Q quit", "", "Log:"]
        panel += ["  " + s for s in self.msgs]
        if self.over:
            panel += ["", "GAME OVER - R to restart, Q to quit"]
        out = ["\x1b[2J\x1b[H"]
        for i in range(VIEW):
            out.append(lines[i] + "  " + (panel[i] if i < len(panel) else ""))
        sys.stdout.write("\n".join(out) + "\n")
        sys.stdout.flush()


def main():
    game = Game()
    while True:
        game.draw()
        k = read_key()
        if k is None:
            continue
        k = k.lower()
        if k in ("q", "\x03"):
            break
        if k == "r":
            game = Game()
            continue
        if k in DIRS:
            game.move(*DIRS[k])
    print("Thanks for playing!")


if __name__ == "__main__":
    main()