import tkinter as tk
import random

CELL = 20
COLS, ROWS = 24, 24
SPEEDS = {"Easy": 200, "Medium": 130, "Hard": 80}


class SnakeGame:
    def __init__(self, root):
        self.root = root
        root.title("Snake")
        self.canvas = tk.Canvas(root, width=COLS * CELL, height=ROWS * CELL,
                                bg="black", highlightthickness=0)
        self.canvas.pack()
        top = tk.Frame(root)
        top.pack(fill="x")
        self.score_var = tk.StringVar(value="Score: 0")
        tk.Label(top, textvariable=self.score_var, font=("Arial", 12, "bold")).pack(side="left", padx=8)
        self.level_var = tk.StringVar(value="Medium")
        for name in SPEEDS:
            tk.Radiobutton(top, text=name, variable=self.level_var, value=name).pack(side="left")
        tk.Button(top, text="Start / Restart", command=self.start).pack(side="left", padx=8)
        root.bind("<Key>", self.on_key)
        self.running = False
        self.after_id = None
        self.snake = []
        self.draw_text("Pick a difficulty, then press Start")
        root.mainloop()

    def start(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.snake = [(COLS // 2, ROWS // 2)]
        self.direction = (1, 0)
        self.next_dir = self.direction
        self.score = 0
        self.score_var.set("Score: 0")
        self.food = self.spawn_food()
        self.delay = SPEEDS[self.level_var.get()]
        self.running = True
        self.draw()
        self.after_id = self.root.after(self.delay, self.tick)

    def spawn_food(self):
        while True:
            pos = (random.randrange(COLS), random.randrange(ROWS))
            if pos not in self.snake:
                return pos

    def on_key(self, event):
        mapping = {"Up": (0, -1), "Down": (0, 1), "Left": (-1, 0), "Right": (1, 0),
                   "w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}
        d = mapping.get(event.keysym)
        if d and (d[0] != -self.direction[0] or d[1] != -self.direction[1]):
            self.next_dir = d

    def tick(self):
        self.after_id = None
        if not self.running:
            return
        self.direction = self.next_dir
        hx, hy = self.snake[0]
        nx, ny = hx + self.direction[0], hy + self.direction[1]
        if nx < 0 or nx >= COLS or ny < 0 or ny >= ROWS or (nx, ny) in self.snake:
            self.running = False
            self.draw_text("Game Over!  Score: %d\nPress Start to play again" % self.score)
            return
        self.snake.insert(0, (nx, ny))
        if (nx, ny) == self.food:
            self.score += 1
            self.score_var.set("Score: %d" % self.score)
            self.food = self.spawn_food()
        else:
            self.snake.pop()
        self.draw()
        self.after_id = self.root.after(self.delay, self.tick)

    def draw(self):
        c = self.canvas
        c.delete("all")
        fx, fy = self.food
        c.create_rectangle(fx * CELL + 3, fy * CELL + 3,
                           fx * CELL + CELL - 3, fy * CELL + CELL - 3,
                           fill="red", outline="")
        for i, (x, y) in enumerate(self.snake):
            color = "#00cc44" if i == 0 else "lime"
            c.create_rectangle(x * CELL + 1, y * CELL + 1,
                               x * CELL + CELL - 1, y * CELL + CELL - 1,
                               fill=color, outline="")

    def draw_text(self, msg):
        self.canvas.delete("all")
        self.canvas.create_text(COLS * CELL // 2, ROWS * CELL // 2, text=msg,
                                fill="white", font=("Arial", 14), justify="center")


if __name__ == "__main__":
    SnakeGame(tk.Tk())