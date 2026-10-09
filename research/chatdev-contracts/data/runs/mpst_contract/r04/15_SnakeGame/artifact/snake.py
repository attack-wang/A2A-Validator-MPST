import random
import tkinter as tk

CELL = 20
COLS = 30
ROWS = 20
BAR_HEIGHT = 40

BLACK = "#121212"
GRID = "#202020"
WHITE = "#f0f0f0"
GRAY = "#828282"
GREEN = "#00c850"
DARK_GREEN = "#008232"
RED = "#dc3c3c"
BAR = "#282828"

# (name, milliseconds per move)
DIFFICULTIES = [("Easy", 166), ("Medium", 100), ("Hard", 66), ("Insane", 45)]


class Snake:
    def __init__(self):
        self.body = [(COLS // 2, ROWS // 2)]
        self.direction = (1, 0)
        self.next_direction = None
        self.pending_growth = 0

    def turn(self, direction):
        if self.next_direction is None:
            if (direction[0] * -1, direction[1] * -1) != self.direction:
                self.next_direction = direction

    def step(self):
        if self.next_direction is not None:
            if (self.next_direction[0] * -1,
                    self.next_direction[1] * -1) != self.direction:
                self.direction = self.next_direction
            self.next_direction = None
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
            return False
        blocked = self.body if self.pending_growth else self.body[:-1]
        if new_head in blocked:
            return False
        self.body.insert(0, new_head)
        if self.pending_growth:
            self.pending_growth -= 1
        else:
            self.body.pop()
        return True

    def grow(self):
        self.pending_growth += 1


class Game:
    def __init__(self, root):
        self.root = root
        self.width = COLS * CELL
        self.height = ROWS * CELL
        self.canvas = tk.Canvas(root, width=self.width,
                                height=self.height + BAR_HEIGHT,
                                bg=BLACK, highlightthickness=0)
        self.canvas.pack()
        root.title("Snake")
        root.resizable(False, False)
        root.protocol("WM_DELETE_WINDOW", self.quit)
        self.delay = DIFFICULTIES[1][1]
        self.difficulty_name = DIFFICULTIES[1][0]
        self.state = "menu"
        self.menu_index = 1
        self.move_job = None
        self.reset()
        root.bind("<Key>", self.on_key)
        self.draw_menu()

    def reset(self):
        self.snake = Snake()
        self.score = 0
        self.alive = True
        self.won = False
        self.food = self.spawn_food()

    def spawn_food(self):
        free = [(x, y) for x in range(COLS) for y in range(ROWS)
                if (x, y) not in self.snake.body]
        return random.choice(free) if free else None

    def quit(self):
        self.cancel_move()
        self.root.destroy()

    def cancel_move(self):
        if self.move_job is not None:
            self.root.after_cancel(self.move_job)
            self.move_job = None

    def on_key(self, event):
        key = event.keysym.lower()
        if self.state == "menu":
            if key in ("up", "w"):
                self.menu_index = (self.menu_index - 1) % len(DIFFICULTIES)
                self.draw_menu()
            elif key in ("down", "s"):
                self.menu_index = (self.menu_index + 1) % len(DIFFICULTIES)
                self.draw_menu()
            elif key in ("return", "space"):
                self.start_game()
            elif key == "escape":
                self.quit()
        elif self.state == "playing":
            if key in ("up", "w"):
                self.snake.turn((0, -1))
            elif key in ("down", "s"):
                self.snake.turn((0, 1))
            elif key in ("left", "a"):
                self.snake.turn((-1, 0))
            elif key in ("right", "d"):
                self.snake.turn((1, 0))
            elif key == "escape":
                self.quit()
        elif self.state == "over":
            if key in ("return", "space"):
                self.start_game()
            elif key == "escape":
                self.quit()

    def start_game(self):
        name, delay = DIFFICULTIES[self.menu_index]
        self.difficulty_name = name
        self.delay = delay
        self.reset()
        self.state = "playing"
        self.draw()
        self.schedule_move()

    def schedule_move(self):
        self.move_job = self.root.after(self.delay, self.tick)

    def tick(self):
        self.move_job = None
        if self.state != "playing":
            return
        if not self.snake.step():
            self.game_over()
            return
        if self.snake.body[0] == self.food:
            self.score += 1
            self.snake.grow()
            self.food = self.spawn_food()
            if self.food is None:
                self.won = True
                self.game_over()
                return
        self.draw()
        self.schedule_move()

    def game_over(self):
        self.state = "over"
        self.draw()
        self.draw_game_over()

    def draw_cell(self, x, y, color):
        self.canvas.create_rectangle(x * CELL, y * CELL,
                                     (x + 1) * CELL, (y + 1) * CELL,
                                     fill=color, outline="", width=0)

    def draw(self):
        canvas = self.canvas
        canvas.delete("all")
        for x in range(0, self.width, CELL):
            canvas.create_line(x, 0, x, self.height, fill=GRID)
        for y in range(0, self.height, CELL):
            canvas.create_line(0, y, self.width, y, fill=GRID)
        if self.food is not None:
            self.draw_cell(self.food[0], self.food[1], RED)
        for i, (x, y) in enumerate(self.snake.body):
            self.draw_cell(x, y, DARK_GREEN if i == 0 else GREEN)
        canvas.create_rectangle(0, self.height, self.width,
                                self.height + BAR_HEIGHT,
                                fill=BAR, outline="", width=0)
        info = f"Score: {self.score}    Difficulty: {self.difficulty_name}"
        canvas.create_text(10, self.height + BAR_HEIGHT // 2, text=info,
                           fill=WHITE, anchor="w", font=("Consolas", 14))

    def draw_menu(self):
        canvas = self.canvas
        canvas.delete("all")
        canvas.create_text(self.width // 2, 70, text="SNAKE",
                           fill=GREEN, font=("Consolas", 32, "bold"))
        for i, (name, _) in enumerate(DIFFICULTIES):
            color = GREEN if i == self.menu_index else GRAY
            canvas.create_text(self.width // 2, 140 + i * 34, text=name,
                               fill=color, font=("Consolas", 16))
        canvas.create_text(self.width // 2, self.height - 20,
                           text="Up/Down: choose   Enter: start   Esc: quit",
                           fill=GRAY, font=("Consolas", 12))

    def draw_game_over(self):
        canvas = self.canvas
        canvas.create_rectangle(0, 0, self.width, self.height,
                                fill=BLACK, stipple="gray50", outline="")
        title = "YOU WIN!" if self.won else "GAME OVER"
        color = GREEN if self.won else RED
        canvas.create_text(self.width // 2, 80, text=title, fill=color,
                           font=("Consolas", 30, "bold"))
        canvas.create_text(self.width // 2, 130,
                           text=f"Final Score: {self.score}",
                           fill=WHITE, font=("Consolas", 16))
        canvas.create_text(self.width // 2, 170,
                           text="Enter: play again    Esc: quit",
                           fill=GRAY, font=("Consolas", 12))