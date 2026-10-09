import random
import tkinter as tk
from config import CELL, COLS, ROWS, HUD, WIDTH, HEIGHT, SPEEDS, COLORS

DIRS = {"Up": (0, -1), "Down": (0, 1), "Left": (-1, 0), "Right": (1, 0),
        "w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}


class Snake:
    def __init__(self):
        cx, cy = COLS // 2, ROWS // 2
        self.body = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = (1, 0)
        self.queue = []

    def turn(self, d):
        last = self.queue[-1] if self.queue else self.direction
        if d != last and (d[0] + last[0], d[1] + last[1]) != (0, 0) and len(self.queue) < 2:
            self.queue.append(d)


class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Snake")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT,
                                bg=COLORS["bg"], highlightthickness=0)
        self.canvas.pack()
        self.root.bind("<Key>", self.on_key)
        self.state = "menu"
        self.difficulty = "Medium"
        self.gen = 0
        self.reset()
        self.draw()

    def reset(self):
        self.snake = Snake()
        self.score = 0
        self.won = False
        self.spawn_food()

    def start(self):
        self.reset()
        self.state = "play"
        self.gen += 1
        self.tick(self.gen)

    def spawn_food(self):
        free = [(x, y) for x in range(COLS) for y in range(ROWS)
                if (x, y) not in self.snake.body]
        self.food = random.choice(free) if free else None

    def on_key(self, event):
        k = event.keysym
        if len(k) == 1:
            k = k.lower()
        if k == "Escape":
            if self.state == "play":
                self.state = "menu"
                self.draw()
            else:
                self.root.destroy()
            return
        if self.state == "menu":
            if k in ("1", "2", "3"):
                self.difficulty = {"1": "Easy", "2": "Medium", "3": "Hard"}[k]
                self.start()
        elif self.state == "play":
            if k in DIRS:
                self.snake.turn(DIRS[k])
        elif k == "r":
            self.start()
        elif k == "m":
            self.state = "menu"
            self.draw()
        elif k == "q":
            self.root.destroy()

    def tick(self, gen):
        if self.state != "play" or gen != self.gen:
            return
        self.update()
        self.draw()
        if self.state == "play":
            self.root.after(SPEEDS[self.difficulty], self.tick, gen)

    def update(self):
        s = self.snake
        if s.queue:
            s.direction = s.queue.pop(0)
        hx, hy = s.body[0]
        head = (hx + s.direction[0], hy + s.direction[1])
        if not (0 <= head[0] < COLS and 0 <= head[1] < ROWS):
            self.state = "over"
            return
        eating = head == self.food
        if head in (s.body if eating else s.body[:-1]):
            self.state = "over"
            return
        s.body.insert(0, head)
        if eating:
            self.score += 1
            self.spawn_food()
            if self.food is None:
                self.won = True
                self.state = "over"
        else:
            s.body.pop()

    def draw(self):
        c = self.canvas
        c.delete("all")
        for x in range(0, WIDTH, CELL):
            c.create_line(x, 0, x, ROWS * CELL, fill=COLORS["grid"])
        for y in range(0, ROWS * CELL, CELL):
            c.create_line(0, y, WIDTH, y, fill=COLORS["grid"])
        if self.food:
            fx, fy = self.food
            c.create_rectangle(fx * CELL + 3, fy * CELL + 3,
                               (fx + 1) * CELL - 3, (fy + 1) * CELL - 3,
                               fill=COLORS["food"], outline="")
        for i, (x, y) in enumerate(self.snake.body):
            c.create_rectangle(x * CELL + 1, y * CELL + 1,
                               (x + 1) * CELL - 1, (y + 1) * CELL - 1,
                               fill=COLORS["head"] if i == 0 else COLORS["snake"],
                               outline="")
        c.create_rectangle(0, ROWS * CELL, WIDTH, HEIGHT,
                           fill=COLORS["hud"], outline="")
        c.create_text(10, ROWS * CELL + HUD // 2, anchor="w", fill=COLORS["text"],
                      text=f"Score: {self.score}    Difficulty: {self.difficulty}    "
                           f"Arrows/WASD move - ESC menu")
        if self.state == "menu":
            self.overlay(["SNAKE", "Select difficulty:", "1 - Easy", "2 - Medium",
                          "3 - Hard", "ESC - Quit"])
        elif self.state == "over":
            title = "YOU WIN!" if self.won else "GAME OVER"
            self.overlay([f"{title}   Score: {self.score}",
                          "R - Restart    M - Menu    Q - Quit"])

    def overlay(self, lines):
        c = self.canvas
        c.create_rectangle(0, 0, WIDTH, ROWS * CELL, fill="#000000",
                           outline="", stipple="gray50")
        y = ROWS * CELL // 2 - len(lines) * 16
        for line in lines:
            big = line == "SNAKE" or line.startswith(("GAME OVER", "YOU WIN"))
            c.create_text(WIDTH // 2, y, text=line, fill=COLORS["text"],
                          font=("Consolas", 22 if big else 12,
                                "bold" if big else "normal"))
            y += 40 if big else 26

    def run(self):
        self.root.mainloop()