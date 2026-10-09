import random
import tkinter as tk

from config import *

DIRS = {
    "Up": (0, -1), "Down": (0, 1), "Left": (-1, 0), "Right": (1, 0),
    "w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0),
}


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        cx, cy = COLS // 2, ROWS // 2
        self.body = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = (1, 0)
        self.queue = []
        self.pending = 0

    def turn(self, d):
        last = self.queue[-1] if self.queue else self.direction
        if d == last or (d[0] == -last[0] and d[1] == -last[1]):
            return
        if len(self.queue) < 2:
            self.queue.append(d)

    def step(self):
        if self.queue:
            self.direction = self.queue.pop(0)
        nx, ny = self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1]
        if not (0 <= nx < COLS and 0 <= ny < ROWS):
            return False
        if self.pending:
            self.pending -= 1
        else:
            self.body.pop()
        if (nx, ny) in self.body:
            return False
        self.body.insert(0, (nx, ny))
        return True


class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Snake")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg=BLACK, highlightthickness=0)
        self.canvas.pack()
        self.snake = Snake()
        self.state = "menu"
        self.diff_name = ""
        self.speed = 10
        self.score = 0
        self.food = None
        self._job = None
        self.spawn_food()
        self.root.bind("<Key>", self.on_key)
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.draw()

    def spawn_food(self):
        free = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in self.snake.body]
        self.food = random.choice(free) if free else None

    def reset_run(self):
        self.snake.reset()
        self.score = 0
        self.spawn_food()

    def on_key(self, e):
        k = e.keysym
        if k == "Escape":
            self.quit()
        elif self.state == "menu":
            if k in DIFFICULTIES:
                self.diff_name, self.speed = DIFFICULTIES[k]
                self.reset_run()
                self.state = "play"
                self.draw()
                self.schedule()
        elif self.state == "play":
            if k in DIRS:
                self.snake.turn(DIRS[k])
        elif k == "Return":
            self.reset_run()
            self.state = "play"
            self.draw()
            self.schedule()
        elif k == "m":
            self.state = "menu"
            self.draw()

    def schedule(self):
        if self._job is not None:
            self.root.after_cancel(self._job)
        self._job = self.root.after(max(1, int(1000 / self.speed)), self.tick)

    def tick(self):
        self._job = None
        if self.state != "play":
            return
        if not self.snake.step():
            self.state = "over"
        elif self.food and self.snake.body[0] == self.food:
            self.score += 1
            self.snake.pending += 1
            self.spawn_food()
            if self.food is None:
                self.state = "win"
        self.draw()
        if self.state == "play":
            self.schedule()

    def cell(self, pos, color):
        x, y = pos
        self.canvas.create_rectangle(x * CELL + 1, y * CELL + 1, (x + 1) * CELL - 1, (y + 1) * CELL - 1,
                                     fill=color, outline="")

    def overlay(self, title, msg):
        c = self.canvas
        c.create_rectangle(0, 0, COLS * CELL, ROWS * CELL, fill="#000000", stipple="gray50", outline="")
        cx, cy = COLS * CELL // 2, ROWS * CELL // 2
        c.create_text(cx, cy - 22, text=title, fill=WHITE, font=("Consolas", 22, "bold"))
        c.create_text(cx, cy + 22, text=msg, fill=WHITE, font=("Consolas", 11))

    def draw(self):
        c = self.canvas
        c.delete("all")
        c.create_rectangle(1, 1, COLS * CELL - 1, ROWS * CELL - 1, outline=GRAY, width=2)
        if self.food:
            self.cell(self.food, RED)
        for i, seg in enumerate(self.snake.body):
            self.cell(seg, DARK_GREEN if i == 0 else GREEN)
        c.create_text(10, ROWS * CELL + HUD // 2, anchor="w", fill=WHITE,
                      text=f"Score: {self.score}   Difficulty: {self.diff_name or '-'}",
                      font=("Consolas", 12))
        if self.state == "menu":
            self.overlay("SNAKE", "Pick difficulty: 1 Easy  2 Normal  3 Hard  4 Insane")
        elif self.state == "over":
            self.overlay("GAME OVER", f"Score: {self.score}  |  Enter retry  M menu  Esc quit")
        elif self.state == "win":
            self.overlay("YOU WIN!", f"Score: {self.score}  |  Enter retry  M menu  Esc quit")

    def quit(self):
        if self._job is not None:
            self.root.after_cancel(self._job)
            self._job = None
        self.root.destroy()

    def run(self):
        self.root.mainloop()