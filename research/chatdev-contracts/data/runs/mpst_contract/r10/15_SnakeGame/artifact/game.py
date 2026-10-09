import random
import tkinter as tk

CELL = 20
COLS, ROWS = 30, 20
INFO_H = 40
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL
WINDOW_H = HEIGHT + INFO_H

DIFFICULTIES = {"1": ("Easy", 130), "2": ("Medium", 90), "3": ("Hard", 60)}
DIRS = {
    "Up": (0, -1), "w": (0, -1), "W": (0, -1),
    "Down": (0, 1), "s": (0, 1), "S": (0, 1),
    "Left": (-1, 0), "a": (-1, 0), "A": (-1, 0),
    "Right": (1, 0), "d": (1, 0), "D": (1, 0),
}


class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Snake")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=WINDOW_H,
                                bg="#0f0f0f", highlightthickness=0)
        self.canvas.pack()
        self.root.bind("<Key>", self.on_key)
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.state = "menu"
        self.score = 0
        self.snake = []
        self.food = None
        self.direction = (1, 0)
        self.pending = None
        self.speed = 130
        self.diff_name = "Easy"
        self.draw_menu()

    def quit(self):
        self.root.destroy()

    def reset(self, speed, name):
        self.speed = speed
        self.diff_name = name
        self.snake = [(COLS // 2, ROWS // 2)]
        self.direction = (1, 0)
        self.pending = None
        self.score = 0
        self.food = self.spawn_food()

    def spawn_food(self):
        free = [(x, y) for x in range(COLS) for y in range(ROWS)
                if (x, y) not in self.snake]
        return random.choice(free) if free else None

    def on_key(self, event):
        key = event.keysym
        if key in ("q", "Q"):
            if self.state != "play":
                self.quit()
            return
        if self.state == "play":
            if key in DIRS:
                nd = DIRS[key]
                if nd[0] + self.direction[0] != 0 or nd[1] + self.direction[1] != 0:
                    self.pending = nd
        elif key in DIFFICULTIES:
            name, speed = DIFFICULTIES[key]
            self.reset(speed, name)
            self.state = "play"

    def step(self):
        if self.pending:
            self.direction = self.pending
            self.pending = None
        hx, hy = self.snake[0]
        head = (hx + self.direction[0], hy + self.direction[1])
        eating = head == self.food
        body = self.snake if eating else self.snake[:-1]
        if not (0 <= head[0] < COLS and 0 <= head[1] < ROWS) or head in body:
            self.state = "over"
            return
        self.snake.insert(0, head)
        if eating:
            self.score += 1
            self.food = self.spawn_food()
            if self.food is None:
                self.state = "over"
        else:
            self.snake.pop()

    def rect(self, pos):
        x, y = pos
        return (x * CELL + 1, INFO_H + y * CELL + 1, CELL - 2, CELL - 2)

    def draw(self):
        c = self.canvas
        c.delete("all")
        c.create_rectangle(0, INFO_H, WIDTH, WINDOW_H, fill="#232323", width=0)
        if self.food:
            c.create_rectangle(*self.rect(self.food), fill="#dc4646", width=0)
        for i, seg in enumerate(self.snake):
            c.create_rectangle(*self.rect(seg),
                               fill="#3ca064" if i == 0 else "#5ac878", width=0)
        c.create_text(10, INFO_H // 2, anchor="w", fill="#ebebeb",
                      text="Score: {}    Difficulty: {}".format(self.score, self.diff_name),
                      font=("Helvetica", 14))
        if self.state == "over":
            cx, cy = WIDTH // 2, INFO_H + HEIGHT // 2
            c.create_text(cx, cy - 20, fill="#ff5a5a", font=("Helvetica", 24, "bold"),
                          text="Game Over  -  Score: {}".format(self.score))
            c.create_text(cx, cy + 22, fill="#c8c8c8", font=("Helvetica", 12),
                          text="1/2/3 = new game (choose difficulty)   Q = quit")

    def draw_menu(self):
        c = self.canvas
        c.delete("all")
        c.create_text(WIDTH // 2, 70, text="SNAKE", fill="#5ac878",
                      font=("Helvetica", 32, "bold"))
        y = 150
        for key, (name, speed) in DIFFICULTIES.items():
            c.create_text(WIDTH // 2, y, fill="#ebebeb", font=("Helvetica", 14),
                          text="[{}]  {}  ({} ms per step)".format(key, name, speed))
            y += 36
        c.create_text(WIDTH // 2, y + 15, fill="#aaaaaa", font=("Helvetica", 12),
                      text="Arrows/WASD to move - eat red food - avoid walls and yourself")

    def loop(self):
        if self.state == "play":
            self.step()
            self.draw()
            self.root.after(self.speed, self.loop)
        else:
            self.root.after(100, self.loop)

    def run(self):
        self.loop()
        self.root.mainloop()