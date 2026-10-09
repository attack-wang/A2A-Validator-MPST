# Classic Snake game (Python standard library only, tkinter GUI)
import random
import tkinter as tk

CELL = 20
COLS, ROWS = 30, 22
HUD = 40
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL + HUD

DIFFICULTIES = [("Easy", 7), ("Medium", 12), ("Hard", 18)]

BLACK = "#121212"
GRID = "#202020"
GREEN = "#00c800"
DARK_GREEN = "#009600"
RED = "#dc3232"
WHITE = "#f0f0f0"
GRAY = "#a0a0a0"
YELLOW = "#ffdc00"
HUD_BG = "#2d2d2d"

DIRS = {
    "Up": (0, -1), "Down": (0, 1), "Left": (-1, 0), "Right": (1, 0),
    "w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0),
    "W": (0, -1), "S": (0, 1), "A": (-1, 0), "D": (1, 0),
}


class SnakeApp:
    def __init__(self, root):
        self.root = root
        root.title("Snake")
        root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                                bg=BLACK, highlightthickness=0)
        self.canvas.pack()
        root.bind("<Key>", self.on_key)
        self.state = "menu"
        self.selected = 1
        self.show_menu()

    # ----- input -----
    def on_key(self, event):
        key = event.keysym
        if self.state == "menu":
            if key in ("Up", "w", "W"):
                self.selected = (self.selected - 1) % len(DIFFICULTIES)
                self.show_menu()
            elif key in ("Down", "s", "S"):
                self.selected = (self.selected + 1) % len(DIFFICULTIES)
                self.show_menu()
            elif key in ("1", "2", "3"):
                self.selected = int(key) - 1
                self.show_menu()
            elif key in ("Return", "space"):
                self.start_game()
        elif self.state == "playing":
            if key == "Escape":
                self.show_menu()
            else:
                d = DIRS.get(key)
                if d and len(self.pending) < 2:
                    self.pending.append(d)
        elif self.state == "gameover":
            if key in ("r", "R"):
                self.start_game()
            elif key in ("q", "Q", "Escape"):
                self.show_menu()

    # ----- screens -----
    def show_menu(self):
        self.state = "menu"
        c = self.canvas
        c.delete("all")
        c.create_text(WIDTH // 2, 70, text="SNAKE", fill=WHITE,
                      font=("Helvetica", 40, "bold"))
        c.create_text(WIDTH // 2, 160, text="Select difficulty (Up/Down, Enter):",
                      fill=WHITE, font=("Helvetica", 14))
        for i, (name, speed) in enumerate(DIFFICULTIES):
            color = YELLOW if i == self.selected else GRAY
            prefix = "> " if i == self.selected else "   "
            c.create_text(WIDTH // 2, 220 + i * 40, text=prefix + name, fill=color,
                          font=("Helvetica", 18, "bold" if i == self.selected else "normal"))
        c.create_text(WIDTH // 2, 380,
                      text="Arrows/WASD to move. Eat food, avoid walls and yourself.",
                      fill=GRAY, font=("Helvetica", 11))
        c.create_text(WIDTH // 2, 405, text="Esc during game returns to menu.",
                      fill=GRAY, font=("Helvetica", 11))

    def start_game(self):
        name, speed = DIFFICULTIES[self.selected]
        self.speed = speed
        self.level_name = name
        self.snake = [(COLS // 2, ROWS // 2)]
        self.direction = (1, 0)
        self.pending = []
        self.score = 0
        self.food = self.spawn_food()
        self.state = "playing"
        self.draw()
        self.root.after(1000 // self.speed, self.tick)

    def spawn_food(self):
        free = [(x, y) for x in range(COLS) for y in range(ROWS)
                if (x, y) not in self.snake]
        return random.choice(free) if free else None

    # ----- game loop -----
    def tick(self):
        if self.state != "playing":
            return
        self.step()
        if self.state == "playing":
            self.draw()
            self.root.after(1000 // self.speed, self.tick)

    def step(self):
        while self.pending:
            d = self.pending.pop(0)
            if d != (-self.direction[0], -self.direction[1]):
                self.direction = d
                break
        dx, dy = self.direction
        head = (self.snake[0][0] + dx, self.snake[0][1] + dy)
        if not (0 <= head[0] < COLS and 0 <= head[1] < ROWS):
            self.game_over()
            return
        growing = head == self.food
        body = self.snake if growing else self.snake[:-1]
        if head in body:
            self.game_over()
            return
        self.snake.insert(0, head)
        if growing:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def game_over(self):
        self.state = "gameover"
        self.draw()
        c = self.canvas
        c.create_rectangle(0, HEIGHT // 2 - 70, WIDTH, HEIGHT // 2 + 70,
                           fill=BLACK, outline=RED, width=2)
        c.create_text(WIDTH // 2, HEIGHT // 2 - 40, text="GAME OVER",
                      fill=RED, font=("Helvetica", 32, "bold"))
        c.create_text(WIDTH // 2, HEIGHT // 2, text="Final Score: %d" % self.score,
                      fill=WHITE, font=("Helvetica", 18))
        c.create_text(WIDTH // 2, HEIGHT // 2 + 40, text="R = Restart    Q = Menu",
                      fill=GRAY, font=("Helvetica", 13))

    # ----- rendering -----
    def draw(self):
        c = self.canvas
        board_h = HEIGHT - HUD
        c.delete("all")
        for x in range(0, WIDTH + 1, CELL):
            c.create_line(x, 0, x, board_h, fill=GRID)
        for y in range(0, board_h + 1, CELL):
            c.create_line(0, y, WIDTH, y, fill=GRID)
        if self.food:
            fx, fy = self.food
            c.create_rectangle(fx * CELL + 2, fy * CELL + 2,
                               fx * CELL + CELL - 2, fy * CELL + CELL - 2,
                               fill=RED, outline="")
        for i, (sx, sy) in enumerate(self.snake):
            color = DARK_GREEN if i == 0 else GREEN
            c.create_rectangle(sx * CELL + 1, sy * CELL + 1,
                               sx * CELL + CELL - 1, sy * CELL + CELL - 1,
                               fill=color, outline="")
        c.create_rectangle(0, board_h, WIDTH, HEIGHT, fill=HUD_BG, outline="")
        c.create_rectangle(0, 0, WIDTH - 1, HEIGHT - 1, outline=GRAY, width=2)
        c.create_text(10, board_h + HUD // 2, text="Score: %d" % self.score,
                      fill=WHITE, anchor="w", font=("Helvetica", 14, "bold"))
        c.create_text(WIDTH - 10, board_h + HUD // 2, text="Level: %s" % self.level_name,
                      fill=WHITE, anchor="e", font=("Helvetica", 14, "bold"))


def main():
    root = tk.Tk()
    SnakeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()