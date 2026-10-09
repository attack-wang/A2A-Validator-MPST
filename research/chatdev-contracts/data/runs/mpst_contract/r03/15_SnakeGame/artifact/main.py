import random
import tkinter as tk

CELL = 20
COLS, ROWS = 24, 24
DIFFICULTIES = {"Easy": 200, "Medium": 130, "Hard": 80}


class SnakeGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Snake")
        self.resizable(False, False)
        self.canvas = tk.Canvas(self, width=COLS * CELL, height=ROWS * CELL,
                                bg="#101010", highlightthickness=0)
        self.canvas.pack()
        self.status = tk.Label(self, font=("Arial", 12), text="Score: 0  Best: 0")
        self.status.pack(fill=tk.X)
        self.menu = tk.Frame(self)
        self.menu.pack(fill=tk.X)
        self.best = 0
        self.running = False
        self._job = None
        for name, speed in DIFFICULTIES.items():
            tk.Button(self.menu, text=name, width=10,
                      command=lambda s=speed: self.start(s)).pack(
                side=tk.LEFT, expand=True, padx=4, pady=4)
        self.bind_all("<Key>", self.on_key)
        self.draw_message("SNAKE\n\nChoose a difficulty to start\nArrows or WASD to move")

    def start(self, speed):
        if self._job is not None:
            self.after_cancel(self._job)
            self._job = None
        self.speed = speed
        self.score = 0
        self.snake = [(COLS // 2, ROWS // 2)]
        self.direction = (1, 0)
        self.pending = self.direction
        self.spawn_food()
        self.running = True
        self.render()
        self._job = self.after(self.speed, self.tick)

    def on_key(self, e):
        dirs = {"Up": (0, -1), "Down": (0, 1), "Left": (-1, 0), "Right": (1, 0),
                "w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}
        d = dirs.get(e.keysym) or dirs.get(e.char.lower())
        if d and self.running and (d[0] + self.direction[0],
                                   d[1] + self.direction[1]) != (0, 0):
            self.pending = d

    def spawn_food(self):
        free = [(x, y) for x in range(COLS) for y in range(ROWS)
                if (x, y) not in self.snake]
        self.food = random.choice(free) if free else None

    def tick(self):
        if not self.running:
            self._job = None
            return
        self.direction = self.pending
        nx = self.snake[0][0] + self.direction[0]
        ny = self.snake[0][1] + self.direction[1]
        if not (0 <= nx < COLS and 0 <= ny < ROWS) or (nx, ny) in self.snake[:-1]:
            self.game_over()
            return
        self.snake.insert(0, (nx, ny))
        if (nx, ny) == self.food:
            self.score += 1
            self.spawn_food()
        else:
            self.snake.pop()
        self.render()
        self._job = self.after(self.speed, self.tick)

    def render(self):
        c = self.canvas
        c.delete("all")
        c.create_rectangle(0, 0, COLS * CELL, ROWS * CELL, outline="#333")
        if self.food:
            x, y = self.food
            c.create_oval(x * CELL + 3, y * CELL + 3,
                          (x + 1) * CELL - 3, (y + 1) * CELL - 3,
                          fill="#e74c3c", outline="")
        for i, (x, y) in enumerate(self.snake):
            color = "#27ae60" if i == 0 else "#2ecc71"
            c.create_rectangle(x * CELL + 1, y * CELL + 1,
                               (x + 1) * CELL - 1, (y + 1) * CELL - 1,
                               fill=color, outline="")
        self.status.config(text="Score: %d  Best: %d" % (self.score, self.best))

    def game_over(self):
        self.running = False
        if self._job is not None:
            self.after_cancel(self._job)
            self._job = None
        self.best = max(self.best, self.score)
        self.render()
        self.draw_message("GAME OVER\n\nScore: %d\n\nChoose a difficulty to play again"
                          % self.score)

    def draw_message(self, text):
        self.canvas.create_text(COLS * CELL / 2, ROWS * CELL / 2, text=text,
                                fill="white", font=("Arial", 16, "bold"),
                                justify=tk.CENTER)


if __name__ == "__main__":
    SnakeGame().mainloop()