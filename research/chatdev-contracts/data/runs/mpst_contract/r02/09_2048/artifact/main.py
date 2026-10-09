import tkinter as tk

from game import Game

CELL_SIZE = 100
GAP = 10
GRID_SIZE = 4
HEADER = 60
WIDTH = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * GAP
HEIGHT = WIDTH + HEADER

BG_COLOR = "#bbada0"
TEXT_COLOR = "#776e65"
LIGHT_TEXT = "#f9f6f2"

TILE_COLORS = {
    2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
    32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
    512: "#edc850", 1024: "#edc53f", 2048: "#edc22e",
}

KEY_MAP = {
    "left": "left", "a": "left",
    "right": "right", "d": "right",
    "up": "up", "w": "up",
    "down": "down", "s": "down",
}


class GameApp:
    def __init__(self, root):
        self.root = root
        root.title("2048")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                                bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack()
        self.game = Game(GRID_SIZE)
        root.bind("<Key>", self.on_key)
        self.draw()

    def on_key(self, event):
        key = event.keysym.lower()
        if key in KEY_MAP:
            self.game.move(KEY_MAP[key])
        elif key == "r":
            self.game.reset()
        elif key == "q":
            self.root.destroy()
            return
        self.draw()

    def draw(self):
        c = self.canvas
        c.delete("all")
        c.create_text(GAP, HEADER // 2, anchor="w", fill=TEXT_COLOR,
                      text="Score: {}".format(self.game.score),
                      font=("Helvetica", 16, "bold"))
        c.create_text(WIDTH - GAP, HEADER // 2, anchor="e", fill=TEXT_COLOR,
                      text="Highest tile: {}".format(self.game.best),
                      font=("Helvetica", 16, "bold"))
        for r in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = GAP + col * (CELL_SIZE + GAP)
                y = HEADER + GAP + r * (CELL_SIZE + GAP)
                value = self.game.grid[r][col]
                fill = TILE_COLORS.get(value, BG_COLOR if value == 0 else "#3c3a32")
                c.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE,
                                   fill=fill, width=0)
                if value:
                    size = 30 if value < 100 else 26 if value < 1000 else 22
                    color = TEXT_COLOR if value <= 4 else LIGHT_TEXT
                    c.create_text(x + CELL_SIZE // 2, y + CELL_SIZE // 2,
                                  text=str(value), fill=color,
                                  font=("Helvetica", size, "bold"))
        if not self.game.can_move():
            c.create_rectangle(GAP, HEADER + GAP, WIDTH - GAP, HEIGHT - GAP,
                               fill="#eee4da", stipple="gray50", width=0)
            cx, cy = WIDTH // 2, HEADER + WIDTH // 2
            c.create_text(cx, cy - 22, text="Game over!", fill=TEXT_COLOR,
                          font=("Helvetica", 26, "bold"))
            c.create_text(cx, cy + 22, text="Press R to restart, Q to quit",
                          fill=TEXT_COLOR, font=("Helvetica", 14))


def main():
    root = tk.Tk()
    GameApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()