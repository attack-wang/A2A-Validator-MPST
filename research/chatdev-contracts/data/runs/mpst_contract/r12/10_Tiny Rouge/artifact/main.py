import random
import tkinter as tk

SIZE = 80
TILE = 9
WALL, FLOOR, DOOR = 0, 1, 2


class Game:
    def __init__(self, root):
        self.root = root
        root.title("Tower of the Sorcerer - Roguelike")
        self.status = tk.Label(root, font=("Consolas", 11), anchor="w")
        self.status.pack(fill="x")
        self.canvas = tk.Canvas(root, width=SIZE * TILE, height=SIZE * TILE,
                                bg="black", highlightthickness=0)
        self.canvas.pack()
        root.bind("<Key>", self.on_key)
        self.new_game()
        self.draw()

    def new_game(self):
        self.level = 1
        self.maxhp = 100
        self.hp = 100
        self.last_monster = None
        self.game_over = False
        self.build_level()

    def build_level(self):
        n = SIZE
        g = [[WALL] * n for _ in range(n)]
        sx, sy, tx, ty = 1, 1, n - 2, n - 2
        x, y, steps = sx, sy, 0
        g[y][x] = FLOOR
        # Biased random walk carves a guaranteed path from start to door.
        while (x, y) != (tx, ty):
            steps += 1
            dx = (tx > x) - (tx < x)
            dy = (ty > y) - (ty < y)
            if steps > 20000:
                while x != tx:
                    x += 1
                    g[y][x] = FLOOR
                while y != ty:
                    y += 1
                    g[y][x] = FLOOR
                break
            if random.random() < 0.8:
                if dx and (not dy or random.random() < 0.5):
                    x += dx
                elif dy:
                    y += dy
                else:
                    x += dx
            else:
                if dy:
                    x += random.choice((-1, 1))
                elif dx:
                    y += random.choice((-1, 1))
            x = max(1, min(n - 2, x))
            y = max(1, min(n - 2, y))
            g[y][x] = FLOOR
        for yy in range(1, n - 1):
            row = g[yy]
            for xx in range(1, n - 1):
                if row[xx] == WALL and random.random() < 0.45:
                    row[xx] = FLOOR
        g[ty][tx] = DOOR
        self.grid = g
        self.door = (tx, ty)
        self.px, self.py = sx, sy
        floors = [(xx, yy) for yy in range(1, n - 1) for xx in range(1, n - 1)
                  if g[yy][xx] == FLOOR and (xx, yy) != (sx, sy)]
        random.shuffle(floors)
        self.entities = {}
        nm = 12 + self.level * 3
        nc = 4 + self.level
        for xx, yy in floors[:nm]:
            self.entities[(xx, yy)] = ("M", random.randint(self.level * 5, self.level * 15),
                                       random.randint(1, self.level * 3))
        for xx, yy in floors[nm:nm + nc]:
            self.entities[(xx, yy)] = ("C",)

    def on_key(self, e):
        k = e.keysym.lower()
        if self.game_over:
            if k == "r":
                self.new_game()
                self.draw()
            return
        d = {"w": (0, -1), "a": (-1, 0), "s": (0, 1), "d": (1, 0),
             "up": (0, -1), "left": (-1, 0), "down": (0, 1), "right": (1, 0)}.get(k)
        if not d:
            return
        nx, ny = self.px + d[0], self.py + d[1]
        if not (0 <= nx < SIZE and 0 <= ny < SIZE) or self.grid[ny][nx] == WALL:
            return
        ent = self.entities.pop((nx, ny), None)
        if ent and ent[0] == "M":
            self.hp -= ent[1]
            self.last_monster = (ent[1], ent[2])
            if self.hp <= 0:
                self.hp = 0
                self.game_over = True
                self.px, self.py = nx, ny
                self.draw()
                return
        elif ent and ent[0] == "C":
            self.hp = min(self.maxhp, self.hp + random.randint(20, 30))
        self.px, self.py = nx, ny
        if self.grid[ny][nx] == DOOR:
            self.level += 1
            self.build_level()
        self.draw()

    def draw(self):
        c = self.canvas
        c.delete("all")
        colors = {WALL: "#3a3a3a", FLOOR: "#c8c8c8", DOOR: "#00aa44"}
        for y in range(SIZE):
            row = self.grid[y]
            base = y * TILE
            for x in range(SIZE):
                c.create_rectangle(x * TILE, base, (x + 1) * TILE, base + TILE,
                                   fill=colors[row[x]], width=0)
        for (x, y), ent in self.entities.items():
            col = "#dd2222" if ent[0] == "M" else "#ffcc00"
            c.create_rectangle(x * TILE + 1, y * TILE + 1,
                               (x + 1) * TILE - 1, (y + 1) * TILE - 1,
                               fill=col, width=0)
        c.create_rectangle(self.px * TILE + 1, self.py * TILE + 1,
                           (self.px + 1) * TILE - 1, (self.py + 1) * TILE - 1,
                           fill="#0066cc", width=0)
        if self.game_over:
            c.create_text(SIZE * TILE // 2, SIZE * TILE // 2,
                          text="GAME OVER\nPress R to restart", fill="white",
                          font=("Consolas", 26, "bold"), justify="center")
        m = "none"
        if self.last_monster:
            m = "HP %d  ATK %d" % self.last_monster
        self.status.config(text="Level: %d    HP: %d/%d    Last monster: %s    "
                                "[W/A/S/D move | R restart]" %
                                (self.level, self.hp, self.maxhp, m))


def main():
    root = tk.Tk()
    Game(root)
    root.mainloop()


if __name__ == "__main__":
    main()