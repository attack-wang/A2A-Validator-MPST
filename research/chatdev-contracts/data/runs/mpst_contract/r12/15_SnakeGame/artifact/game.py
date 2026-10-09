import tkinter as tk

from settings import (CELL, COLS, ROWS, HUD, WIDTH, HEIGHT,
                      DIFFICULTIES, COLORS)
from snake import Snake
from food import Food

MENU, PLAYING, GAME_OVER = "menu", "playing", "game_over"

DIRECTIONS = {
    "up": (0, -1), "w": (0, -1),
    "down": (0, 1), "s": (0, 1),
    "left": (-1, 0), "a": (-1, 0),
    "right": (1, 0), "d": (1, 0),
}

FONT = ("Helvetica", 12)


class Game:
    def __init__(self, root):
        self.root = root
        root.title("Snake")
        root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                                bg=COLORS["bg"], highlightthickness=0)
        self.canvas.pack()
        self.state = MENU
        self.diff_name, self.interval = DIFFICULTIES["2"]
        self.snake = Snake()
        self.food = Food(self.snake)
        self.score = 0
        self._after_id = None
        root.bind("<Key>", self.on_key)
        self.draw()

    def on_key(self, event):
        key = event.keysym.lower()
        if self.state == MENU:
            if key in DIFFICULTIES:
                self.diff_name, self.interval = DIFFICULTIES[key]
                self.start()
            elif key == "escape":
                self.root.destroy()
        elif self.state == PLAYING:
            if key in DIRECTIONS:
                self.snake.set_direction(DIRECTIONS[key])
            elif key == "escape":
                self.cancel_tick()
                self.state = MENU
                self.draw()
        else:
            if key in ("space", "return"):
                self.state = MENU
                self.draw()
            elif key == "escape":
                self.root.destroy()

    def start(self):
        self.cancel_tick()
        self.snake.reset()
        self.food.respawn(self.snake)
        self.score = 0
        self.state = PLAYING
        self.draw()
        self._after_id = self.root.after(self.interval, self.tick)

    def cancel_tick(self):
        if self._after_id is not None:
            self.root.after_cancel(self._after_id)
            self._after_id = None

    def tick(self):
        self._after_id = None
        if self.state != PLAYING:
            return
        self.snake.step()
        if self.snake.hits_wall() or self.snake.hits_self():
            self.state = GAME_OVER
            self.draw()
            return
        if self.food.pos is not None and self.snake.body[0] == self.food.pos:
            self.score += 1
            self.snake.grow_pending += 1
            self.food.respawn(self.snake)
            if self.food.pos is None:
                self.state = GAME_OVER
        self.draw()
        self._after_id = self.root.after(self.interval, self.tick)

    def cell_rect(self, x, y, inset=1):
        return (x * CELL + inset, HUD + y * CELL + inset,
                (x + 1) * CELL - inset, HUD + (y + 1) * CELL - inset)

    def draw(self):
        c = self.canvas
        c.delete("all")
        if self.state == MENU:
            self.draw_menu()
            return
        c.create_rectangle(1, HUD, WIDTH - 1, HUD + ROWS * CELL,
                           outline=COLORS["border"], width=2)
        if self.food.pos is not None:
            c.create_oval(*self.cell_rect(*self.food.pos, 4),
                          fill=COLORS["food"], outline="")
        for i, (x, y) in enumerate(self.snake.body):
            color = COLORS["head"] if i == 0 else COLORS["snake"]
            c.create_rectangle(*self.cell_rect(x, y), fill=color, outline="")
        info = (f"Score: {self.score}   Length: {len(self.snake.body)}   "
                f"Mode: {self.diff_name}")
        c.create_text(10, HUD // 2, anchor="w", text=info,
                      fill=COLORS["text"], font=FONT)
        if self.state == GAME_OVER:
            self.draw_game_over()

    def draw_menu(self):
        c = self.canvas
        cx = WIDTH // 2
        c.create_text(cx, 70, text="SNAKE", fill=COLORS["head"],
                      font=("Helvetica", 32, "bold"))
        lines = ["Select difficulty (press 1-4):"]
        lines += [f"  {k}. {name} - {interval} ms per step"
                  for k, (name, interval) in sorted(DIFFICULTIES.items())]
        lines += ["", "Move: Arrow keys or WASD", "Esc: quit"]
        for i, line in enumerate(lines):
            c.create_text(cx, 150 + i * 26, text=line,
                          fill=COLORS["text"], font=FONT)

    def draw_game_over(self):
        c = self.canvas
        cx = WIDTH // 2
        cy = HEIGHT // 2 - 60
        c.create_rectangle(WIDTH // 4, cy - 20, WIDTH * 3 // 4, cy + 150,
                           fill="#000000", outline=COLORS["border"])
        c.create_text(cx, cy, text="GAME OVER", fill=COLORS["food"],
                      font=("Helvetica", 28, "bold"))
        c.create_text(cx, cy + 60, text=f"Final score: {self.score}",
                      fill=COLORS["text"], font=FONT)
        c.create_text(cx, cy + 90, text="Space/Enter: menu   Esc: quit",
                      fill=COLORS["text"], font=FONT)