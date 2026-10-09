import random
import tkinter as tk

CELL = 24
COLS, ROWS = 24, 18
BAR = 40
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL + BAR

BLACK = "#101014"
GRID = "#1e1e24"
GREEN = "#3cc83c"
HEAD = "#78ff78"
RED = "#e63c3c"
WHITE = "#ebebeb"
GRAY = "#969696"
YELLOW = "#f0c83c"

DIFFICULTIES = [("Easy", 140), ("Medium", 100), ("Hard", 70)]
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)


class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Snake")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT,
                                bg=BLACK, highlightthickness=0)
        self.canvas.pack()
        self.high = 0
        self.difficulty = 1
        self.state = "menu"
        self.root.bind("<Key>", self.on_key)
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.draw_menu()

    def run(self):
        self.root.mainloop()

    def quit(self):
        self.root.destroy()

    def reset(self):
        self.speed = DIFFICULTIES[self.difficulty][1]
        cx, cy = COLS // 2, ROWS // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.dir = RIGHT
        self.queue = []
        self.grow = 0
        self.score = 0
        self.food = self.spawn_food()
        self.state = "playing"
        self.draw()
        self.root.after(self.speed, self.tick)

    def spawn_food(self):
        free = [(x, y) for x in range(COLS) for y in range(ROWS)
                if (x, y) not in self.snake]
        return random.choice(free) if free else None

    def turn(self, d):
        last = self.queue[-1] if self.queue else self.dir
        if (d[0] + last[0], d[1] + last[1]) != (0, 0) and d != last and len(self.queue) < 2:
            self.queue.append(d)

    def step(self):
        if self.queue:
            self.dir = self.queue.pop(0)
        hx, hy = self.snake[0]
        head = (hx + self.dir[0], hy + self.dir[1])
        x, y = head
        body = self.snake if self.grow else self.snake[:-1]
        if x < 0 or x >= COLS or y < 0 or y >= ROWS or head in body:
            self.game_over()
            return
        self.snake.insert(0, head)
        if head == self.food:
            self.score += 1
            self.grow += 1
            self.food = self.spawn_food()
            if self.food is None:
                self.game_over()
                return
        if self.grow:
            self.grow -= 1
        else:
            self.snake.pop()

    def game_over(self):
        self.state = "over"
        self.high = max(self.high, self.score)

    def tick(self):
        if self.state != "playing":
            return
        self.step()
        self.draw()
        if self.state == "playing":
            self.root.after(self.speed, self.tick)

    def on_key(self, event):
        key = event.keysym.lower()
        if self.state == "menu":
            if event.char in ("1", "2", "3"):
                self.difficulty = int(event.char) - 1
                self.reset()
        elif self.state == "playing":
            dirs = {"up": UP, "w": UP, "down": DOWN, "s": DOWN,
                    "left": LEFT, "a": LEFT, "right": RIGHT, "d": RIGHT}
            if key in dirs:
                self.turn(dirs[key])
            elif key == "escape":
                self.state = "menu"
                self.draw_menu()
        elif self.state == "over":
            if key == "r":
                self.reset()
            elif key == "m":
                self.state = "menu"
                self.draw_menu()
            elif key == "escape":
                self.quit()

    def cell(self, x, y):
        return (x * CELL, BAR + y * CELL, (x + 1) * CELL, BAR + (y + 1) * CELL)

    def draw(self):
        c = self.canvas
        c.delete("all")
        c.create_rectangle(0, BAR, WIDTH, HEIGHT, fill=GRID, outline="")
        for i in range(1, COLS):
            c.create_line(i * CELL, BAR, i * CELL, HEIGHT, fill=BLACK)
        for j in range(1, ROWS):
            c.create_line(0, BAR + j * CELL, WIDTH, BAR + j * CELL, fill=BLACK)
        if self.food:
            fx, fy = self.food
            cx, cy = fx * CELL + CELL // 2, BAR + fy * CELL + CELL // 2
            r = CELL // 2 - 2
            c.create_oval(cx - r, cy - r, cx + r, cy + r, fill=RED, outline="")
        for i, (x, y) in enumerate(self.snake):
            c.create_rectangle(*self.cell(x, y),
                               fill=HEAD if i == 0 else GREEN, outline="")
        name = DIFFICULTIES[self.difficulty][0]
        c.create_text(10, BAR // 2, anchor="w", fill=WHITE,
                      text=f"Score: {self.score}   Best: {self.high}   {name}")
        if self.state == "over":
            c.create_rectangle(0, BAR, WIDTH, HEIGHT, fill="#000000", stipple="gray50")
            c.create_text(WIDTH // 2, HEIGHT // 2 - 60, fill=RED, text="GAME OVER",
                          font=("Helvetica", 32, "bold"))
            c.create_text(WIDTH // 2, HEIGHT // 2, fill=WHITE,
                          text=f"Score: {self.score}   Best: {self.high}")
            c.create_text(WIDTH // 2, HEIGHT // 2 + 40, fill=GRAY,
                          text="R: Restart   M: Menu   ESC: Quit")

    def draw_menu(self):
        c = self.canvas
        c.delete("all")
        c.create_text(WIDTH // 2, 80, fill=GREEN, text="SNAKE",
                      font=("Helvetica", 36, "bold"))
        for i, (name, _) in enumerate(DIFFICULTIES):
            color = YELLOW if i == self.difficulty else GRAY
            c.create_text(WIDTH // 2, 160 + i * 34, fill=color, text=f"{i + 1}. {name}")
        c.create_text(WIDTH // 2, 300, fill=WHITE, text="Press 1/2/3 to start")
        c.create_text(WIDTH // 2, 336, fill=GRAY, text="Arrows/WASD to move, ESC to quit")