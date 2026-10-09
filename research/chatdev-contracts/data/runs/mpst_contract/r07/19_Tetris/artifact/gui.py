import tkinter as tk

from tetris import Tetris, COLS, ROWS, COLORS

CELL = 30
PANEL = 190
W, H = COLS * CELL + PANEL, ROWS * CELL
BG = "#0f0f19"
EMPTY = "#1a1a26"
WHITE = "#f0f0f0"
GREY = "#82828c"
DT = 0.04


def rgb(c):
    return "#%02x%02x%02x" % c


def run():
    root = tk.Tk()
    root.title("Tetris")
    root.resizable(False, False)
    canvas = tk.Canvas(root, width=W, height=H, bg=BG, highlightthickness=0)
    canvas.pack()
    game = Tetris()
    state = {"fall": 0.0}

    def rect(x, y, w, h, color):
        canvas.create_rectangle(x + 1, y + 1, x + w - 1, y + h - 1,
                                fill=color, outline="")

    def draw():
        canvas.delete("all")
        bw = COLS * CELL
        for y in range(ROWS):
            for x in range(COLS):
                k = game.board[y][x]
                rect(x * CELL, y * CELL, CELL, CELL,
                     rgb(COLORS[k]) if k else EMPTY)
        for x, y in game.piece.cells():
            if y >= 0:
                rect(x * CELL, y * CELL, CELL, CELL, rgb(COLORS[game.piece.kind]))
        canvas.create_rectangle(0, 0, bw, ROWS * CELL, outline=GREY)
        px = bw + 16
        for i, (label, val) in enumerate((("Score", game.score),
                                          ("Lines", game.lines),
                                          ("Level", game.level))):
            canvas.create_text(px, 28 + i * 30, text=f"{label}: {val}",
                               fill=WHITE, anchor="w", font=("Arial", 13, "bold"))
        canvas.create_text(px, 128, text="Next:", fill=WHITE, anchor="w",
                           font=("Arial", 13, "bold"))
        shape = game.next_piece.shape
        size = 22
        ox = px + (PANEL - 32 - len(shape[0]) * size) // 2
        oy = 148
        for cy, row in enumerate(shape):
            for cx, v in enumerate(row):
                if v:
                    rect(ox + cx * size, oy + cy * size, size, size,
                         rgb(COLORS[game.next_piece.kind]))
        help_y = 268
        for line in ("Left/Right: move", "Down: soft drop", "Up: rotate",
                     "Space: hard drop", "P: pause", "R: restart", "Esc: quit"):
            canvas.create_text(px, help_y, text=line, fill=GREY, anchor="w",
                               font=("Arial", 11))
            help_y += 24
        if game.paused or game.game_over:
            canvas.create_rectangle(0, 0, bw, ROWS * CELL,
                                    fill="#000000", stipple="gray50")
            text = "GAME OVER" if game.game_over else "PAUSED"
            canvas.create_text(bw // 2, ROWS * CELL // 2, text=text,
                               fill="#ff5050", font=("Arial", 26, "bold"))

    def key(e):
        k = e.keysym.lower()
        if k == "escape":
            root.destroy()
            return
        if k == "r":
            game.reset()
            state["fall"] = 0.0
        elif k == "p":
            game.paused = not game.paused
        elif not game.game_over and not game.paused:
            if k == "left":
                game.move(-1)
            elif k == "right":
                game.move(1)
            elif k == "down":
                if game.move(0, 1):
                    game.score += 1
                state["fall"] = 0.0
            elif k == "up":
                game.rotate_piece()
            elif k == "space":
                game.hard_drop()
                state["fall"] = 0.0
        draw()

    def tick():
        if not game.game_over and not game.paused:
            state["fall"] += DT
            if state["fall"] >= game.drop_interval():
                state["fall"] = 0.0
                game.step()
        draw()
        root.after(int(DT * 1000), tick)

    root.bind("<Key>", key)
    draw()
    tick()
    root.mainloop()