import random
import tkinter as tk

CELL = 24
COLS = ROWS = 24
DIFFS = {"1": ("Easy", 130), "2": ("Medium", 80), "3": ("Hard", 50)}
BG = "#0f0f19"
HEAD = "#00ffaa"
BODY = "#00be6e"
FOOD = "#eb4646"
WHITE = "#f0f0f0"
BLUE = "#aac8ff"
GRAY = "#969696"
RED = "#ff5a5a"
KEY_DIRS = {"Up": (0, -1), "w": (0, -1), "W": (0, -1),
            "Down": (0, 1), "s": (0, 1), "S": (0, 1),
            "Left": (-1, 0), "a": (-1, 0), "A": (-1, 0),
            "Right": (1, 0), "d": (1, 0), "D": (1, 0)}


class SnakeGame:
    def __init__(self, root):
        self.root = root
        root.title("Snake")
        root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=COLS * CELL, height=ROWS * CELL,
                                bg=BG, highlightthickness=0)
        self.canvas.pack()
        self.status = tk.Label(root, font=("Consolas", 12), fg=WHITE, bg=BG)
        self.status.pack(fill="x")
        self.state = "menu"
        self.job = None
        self.last_diff = "2"
        root.bind("<Key>", self.on_key)
        root.protocol("WM_DELETE_WINDOW", self.quit)
        self.show_menu()

    def cancel(self):
        if self.job is not None:
            self.root.after_cancel(self.job)
            self.job = None

    def quit(self):
        self.cancel()
        self.root.destroy()

    def text(self, y, msg, color, size=16):
        self.canvas.create_text(COLS * CELL // 2, y, text=msg, fill=color,
                                font=("Consolas", size, "bold"))

    def show_menu(self):
        self.cancel()
        self.state = "menu"
        self.canvas.delete("all")
        self.status.config(text="")
        self.text(120, "SNAKE - Select Difficulty", WHITE, 18)
        self.text(200, "[1] Easy   (slow)", BLUE)
        self.text(240, "[2] Medium (faster)", BLUE)
        self.text(280, "[3] Hard   (fastest)", BLUE)
        self.text(340, "[Q] Quit", GRAY)

    def start(self, key):
        self.cancel()
        self.last_diff = key
        self.name, self.interval = DIFFS[key]
        self.snake = [(COLS // 2, ROWS // 2)]
        self.dirv = self.next_dir = (1, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.state = "play"
        self.draw_board()
        self.job = self.root.after(self.interval, self.tick)

    def game_over(self):
        self.cancel()
        self.state = "over"
        mid = ROWS * CELL // 2
        self.canvas.create_rectangle(0, mid - 70, COLS * CELL, mid + 70,
                                     fill=BG, outline="")
        self.text(mid - 30, "Game Over!  Final Score: %d" % self.score, RED, 18)
        self.text(mid + 30, "[R] Restart   [M] Main Menu   [Q] Quit", WHITE)
        self.status.config(text="Score: %d   Difficulty: %s" % (self.score, self.name))

    def spawn_food(self):
        while True:
            p = (random.randrange(COLS), random.randrange(ROWS))
            if p not in self.snake:
                return p

    def on_key(self, e):
        k = e.keysym
        if k.startswith("KP_"):
            k = k[3:]
        if self.state == "menu":
            if k in DIFFS:
                self.start(k)
            elif k in ("q", "Q"):
                self.quit()
        elif self.state == "play":
            v = KEY_DIRS.get(k)
            if v and (v[0] != -self.next_dir[0] or v[1] != -self.next_dir[1]):
                self.next_dir = v
        elif self.state == "over":
            if k in ("r", "R"):
                self.start(self.last_diff)
            elif k in ("m", "M"):
                self.show_menu()
            elif k in ("q", "Q"):
                self.quit()

    def tick(self):
        if self.state != "play":
            return
        self.dirv = self.next_dir
        nx, ny = self.snake[0][0] + self.dirv[0], self.snake[0][1] + self.dirv[1]
        if not (0 <= nx < COLS and 0 <= ny < ROWS) or (nx, ny) in self.snake:
            self.game_over()
            return
        self.snake.insert(0, (nx, ny))
        if (nx, ny) == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()
        self.draw_board()
        self.job = self.root.after(self.interval, self.tick)

    def draw_board(self):
        self.canvas.delete("all")
        for i, (x, y) in enumerate(self.snake):
            color = HEAD if i == 0 else BODY
            self.canvas.create_rectangle(x * CELL + 1, y * CELL + 1,
                                         (x + 1) * CELL - 1, (y + 1) * CELL - 1,
                                         fill=color, outline="")
        fx, fy = self.food
        self.canvas.create_oval(fx * CELL + 2, fy * CELL + 2,
                                (fx + 1) * CELL - 2, (fy + 1) * CELL - 2,
                                fill=FOOD, outline="")
        self.status.config(text="Score: %d   Difficulty: %s" % (self.score, self.name))


def main():
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()