import random
import tkinter as tk

GRID = 80
CELL = 9
MONSTER_TYPES = [("Slime", 10), ("Bat", 14), ("Skeleton", 20),
                 ("Wizard", 28), ("Ghost", 36)]
COLORS = {"wall": "#3a3a3a", "floor": "#e8e0d0", "player": "#2060ff",
          "monster": "#d02020", "chest": "#c08040", "door": "#ffee00"}


class Game:
    def __init__(self, root):
        self.root = root
        root.title("Tower of the Sorcerer")
        self.canvas = tk.Canvas(root, width=GRID * CELL, height=GRID * CELL,
                                bg="black", highlightthickness=0)
        self.canvas.pack(side="left")
        self.panel = tk.Label(root, font=("Consolas", 11), justify="left",
                              anchor="nw", width=36)
        self.panel.pack(side="right", fill="both", expand=True)
        root.bind("<Key>", self.on_key)
        self.rects = [[self.canvas.create_rectangle(
            x * CELL, y * CELL, (x + 1) * CELL, (y + 1) * CELL, outline="")
            for x in range(GRID)] for y in range(GRID)]
        self.new_game()

    def new_game(self):
        self.hp = 100
        self.level = 1
        self.msg = "W/A/S/D to move. Reach the door!"
        self.last_mon = "None yet"
        self.dead = False
        self.build_level()

    def build_level(self):
        n = GRID
        g = [[1] * n for _ in range(n)]
        g[1][1] = 0
        stack = [(1, 1)]
        while stack:
            x, y = stack[-1]
            for dx, dy in random.sample([(2, 0), (-2, 0), (0, 2), (0, -2)], 4):
                nx, ny = x + dx, y + dy
                if 1 <= nx < n - 1 and 1 <= ny < n - 1 and g[ny][nx]:
                    g[y + dy // 2][x + dx // 2] = 0
                    g[ny][nx] = 0
                    stack.append((nx, ny))
                    break
            else:
                stack.pop()
        for _ in range(700):
            x, y = random.randrange(1, n - 1), random.randrange(1, n - 1)
            if g[y][x] and ((g[y][x - 1] == 0 and g[y][x + 1] == 0) or
                            (g[y - 1][x] == 0 and g[y + 1][x] == 0)):
                g[y][x] = 0
        # Door sits on an odd-odd cell (guaranteed carved floor, connected
        # to the start in the perfect maze); carve defensively anyway.
        self.door = (n - 3, n - 3)
        g[n - 3][n - 3] = 0
        self.grid = g
        self.px, self.py = 1, 1
        self.entities = {}
        floors = [(x, y) for y in range(1, n - 1) for x in range(1, n - 1)
                  if g[y][x] == 0 and (x, y) not in ((1, 1), self.door)
                  and abs(x - 1) + abs(y - 1) > 4]
        random.shuffle(floors)
        mcount = 8 + self.level * 2
        ccount = 3 + self.level
        for i, (x, y) in enumerate(floors):
            if i < mcount:
                name, base = random.choice(MONSTER_TYPES)
                self.entities[(x, y)] = ("monster", name, base + self.level * 3)
            elif i < mcount + ccount:
                self.entities[(x, y)] = ("chest",)
            else:
                break
        self.draw()

    def on_key(self, e):
        k = e.keysym.lower()
        if self.dead:
            if k == "r":
                self.new_game()
            return
        d = {"w": (0, -1), "a": (-1, 0), "s": (0, 1), "d": (1, 0),
             "up": (0, -1), "left": (-1, 0), "down": (0, 1),
             "right": (1, 0)}.get(k)
        if d:
            self.move(*d)

    def move(self, dx, dy):
        nx, ny = self.px + dx, self.py + dy
        if not (0 <= nx < GRID and 0 <= ny < GRID) or self.grid[ny][nx]:
            return
        ent = self.entities.pop((nx, ny), None)
        if ent and ent[0] == "monster":
            _, name, mhp = ent
            self.hp -= mhp
            self.last_mon = "%s  HP %d" % (name, mhp)
            self.msg = "Fought %s! -%d HP" % (name, mhp)
            if self.hp <= 0:
                self.hp = 0
                self.dead = True
                self.msg = "YOU DIED - press R to restart"
        elif ent and ent[0] == "chest":
            heal = random.randint(20, 30)
            self.hp += heal
            self.msg = "Treasure chest! +%d HP" % heal
        if (nx, ny) == self.door and not self.dead:
            self.level += 1
            self.msg = "Descended to level %d!" % self.level
            self.build_level()
            return
        self.px, self.py = nx, ny
        self.draw()

    def draw(self):
        px, py = self.px, self.py
        for y in range(GRID):
            row = self.grid[y]
            for x in range(GRID):
                c = COLORS["wall"] if row[x] else COLORS["floor"]
                ent = self.entities.get((x, y))
                if ent:
                    c = COLORS[ent[0]]
                if (x, y) == self.door:
                    c = COLORS["door"]
                if x == px and y == py:
                    c = COLORS["player"]
                self.canvas.itemconfig(self.rects[y][x], fill=c)
        self.panel.config(text=(
            "Tower of the Sorcerer\n\nLevel: %d\nHP: %d\n\n"
            "Last monster:\n%s\n\n%s\n\nW/A/S/D or arrows: move\n"
            "R: restart after death" % (self.level, self.hp,
                                        self.last_mon, self.msg)))


def main():
    root = tk.Tk()
    Game(root)
    root.mainloop()


if __name__ == "__main__":
    main()