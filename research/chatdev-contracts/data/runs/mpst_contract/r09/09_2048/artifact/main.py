import tkinter as tk

from game import Game2048

CELL = 100
GAP = 10
TOP = 110
BOARD = CELL * 4 + GAP * 5
WIDTH = BOARD
HEIGHT = BOARD + TOP + 10

BG = "#faf8ef"
BOARD_COLOR = "#bbada0"
EMPTY_COLOR = "#cdc1b4"
DARK = "#776e65"
LIGHT = "#f9f6f2"
OVER_FILL = "#3c3a32"

TILE_COLORS = {
    2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
    32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
    512: "#edc850", 1024: "#edc53f", 2048: "#edc22e",
}

KEY_MAP = {
    "Left": "left", "a": "left", "A": "left",
    "Right": "right", "d": "right", "D": "right",
    "Up": "up", "w": "up", "W": "up",
    "Down": "down", "s": "down", "S": "down",
}


class App:
    def __init__(self, root):
        self.game = Game2048()
        self.root = root
        root.title("2048")
        root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                                bg=BG, highlightthickness=0)
        self.canvas.pack()
        for key, direction in KEY_MAP.items():
            root.bind("<%s>" % key, lambda event, d=direction: self.on_key(d))
        for key in ("r", "R"):
            root.bind("<%s>" % key, lambda event: self.restart())
        root.bind("<Escape>", lambda event: root.destroy())
        self.draw()

    def on_key(self, direction):
        if not self.game.game_over():
            self.game.move(direction)
        self.draw()

    def restart(self):
        self.game.reset()
        self.draw()

    def stat_box(self, label, value, cx):
        c = self.canvas
        y0 = 14
        c.create_rectangle(cx - 55, y0, cx + 55, y0 + 64,
                           fill=BOARD_COLOR, width=0)
        c.create_text(cx, y0 + 16, text=label,
                      font=("Arial", 10, "bold"), fill=LIGHT)
        c.create_text(cx, y0 + 42, text=str(value),
                      font=("Arial", 17, "bold"), fill=LIGHT)

    def draw(self):
        c = self.canvas
        c.delete("all")
        c.create_text(GAP + 55, 46, text="2048",
                      font=("Arial", 30, "bold"), fill=DARK)
        self.stat_box("SCORE", self.game.score, WIDTH - 170)
        self.stat_box("BEST TILE", self.game.best_tile, WIDTH - 58)
        c.create_rectangle(GAP, TOP, BOARD, TOP + BOARD - GAP,
                           fill=BOARD_COLOR, width=0)
        for r in range(4):
            for col in range(4):
                x = 2 * GAP + col * (CELL + GAP)
                y = TOP + GAP + r * (CELL + GAP)
                value = self.game.grid[r][col]
                color = EMPTY_COLOR if value == 0 else TILE_COLORS.get(value, OVER_FILL)
                c.create_rectangle(x, y, x + CELL, y + CELL, fill=color, width=0)
                if value:
                    size = 30 if value < 100 else 24 if value < 1000 else 18
                    c.create_text(x + CELL // 2, y + CELL // 2, text=str(value),
                                  font=("Arial", size, "bold"),
                                  fill=DARK if value <= 4 else LIGHT)
        if self.game.best_tile >= 2048 and not self.game.game_over():
            c.create_text(WIDTH // 2, TOP - 12,
                          text="2048 reached! Keep going (R restarts)",
                          font=("Arial", 11), fill=DARK)
        if self.game.game_over():
            c.create_rectangle(0, 0, WIDTH, HEIGHT, fill=BG, stipple="gray50")
            c.create_text(WIDTH // 2, HEIGHT // 2 - 40, text="Game Over!",
                          font=("Arial", 26, "bold"), fill=DARK)
            c.create_text(WIDTH // 2, HEIGHT // 2 + 10,
                          text="Score: %d   Best tile: %d"
                               % (self.game.score, self.game.best_tile),
                          font=("Arial", 13), fill=DARK)
            c.create_text(WIDTH // 2, HEIGHT // 2 + 50,
                          text="Press R to restart - ESC to quit",
                          font=("Arial", 11), fill=DARK)


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()