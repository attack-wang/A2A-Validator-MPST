import random
import tkinter as tk

WIDTH, HEIGHT = 480, 640
FPS = 60
ROWS, COLS = 4, 8
AW, AH, GAP_X, GAP_Y, TOP = 32, 24, 12, 14, 60
COLORS = ("#e65050", "#f0dc50", "#50c8e6", "#f0f0f0")
WHITE, GREEN, RED = "#f0f0f0", "#50dc50", "#e65050"


class Game:
    def __init__(self, root):
        self.root = root
        root.title("Space Invaders")
        self.cv = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                            bg="#0a0a1e", highlightthickness=0)
        self.cv.pack()
        root.bind("<KeyPress>", self.kdown)
        root.bind("<KeyRelease>", self.kup)
        self.keys = set()
        self.reset()
        self.tick()

    def reset(self):
        self.keys.clear()
        self.ship = WIDTH // 2
        self.cool = 0
        self.aliens = [{"x": 40 + c * (AW + GAP_X), "y": TOP + r * (AH + GAP_Y),
                        "row": r} for r in range(ROWS) for c in range(COLS)]
        self.pb, self.ab = [], []
        self.score, self.lives = 0, 3
        self.dir, self.acc, self.ftimer = 1, 0.0, 60
        self.state = "play"

    def kdown(self, e):
        k = e.keysym.lower()
        if k == "escape":
            self.root.destroy()
            return
        if k in ("left", "right", "a", "d"):
            self.keys.add(k)
        if self.state == "play" and k == "space" and self.cool == 0:
            self.pb.append([self.ship - 2, HEIGHT - 60])
            self.cool = 18
        elif self.state != "play" and k == "r":
            self.reset()

    def kup(self, e):
        self.keys.discard(e.keysym.lower())

    def tick(self):
        if self.state == "play":
            self.update()
        self.draw()
        self.root.after(1000 // FPS, self.tick)

    def update(self):
        if "left" in self.keys or "a" in self.keys:
            self.ship -= 5
        if "right" in self.keys or "d" in self.keys:
            self.ship += 5
        self.ship = max(20, min(WIDTH - 20, self.ship))
        if self.cool:
            self.cool -= 1

        step = 0.6 + (ROWS * COLS - len(self.aliens)) * 0.03
        self.acc += step
        while self.acc >= 1:
            self.acc -= 1
            edge = False
            for a in self.aliens:
                a["x"] += self.dir
                if a["x"] <= 0 or a["x"] + AW >= WIDTH:
                    edge = True
            if edge:
                self.dir *= -1
                for a in self.aliens:
                    a["y"] += 16
                break

        self.ftimer -= 1
        if self.ftimer <= 0 and self.aliens:
            a = random.choice(self.aliens)
            self.ab.append([a["x"] + AW // 2 - 2, a["y"] + AH])
            self.ftimer = max(20, 60 - (ROWS * COLS - len(self.aliens)))

        for b in self.pb[:]:
            b[1] -= 8
            if b[1] < 0:
                self.pb.remove(b)
                continue
            for a in self.aliens[:]:
                if (a["x"] < b[0] + 4 and b[0] < a["x"] + AW and
                        a["y"] < b[1] + 10 and b[1] < a["y"] + AH):
                    self.pb.remove(b)
                    self.aliens.remove(a)
                    self.score += (ROWS - a["row"]) * 10
                    break

        for b in self.ab[:]:
            b[1] += 5
            if b[1] > HEIGHT:
                self.ab.remove(b)
                continue
            sx, sy = self.ship - 20, HEIGHT - 50
            if (sx < b[0] + 4 and b[0] < sx + 40 and
                    sy < b[1] + 10 and b[1] < sy + 20):
                self.ab.remove(b)
                self.lives -= 1
                if self.lives <= 0:
                    self.state = "over"

        for a in self.aliens:
            if a["y"] + AH >= HEIGHT - 50:
                self.state = "over"
                break

        if not self.aliens and self.state == "play":
            self.state = "win"

    def draw(self):
        cv = self.cv
        cv.delete("all")
        cv.create_polygon(self.ship, HEIGHT - 50, self.ship + 20, HEIGHT - 30,
                          self.ship - 20, HEIGHT - 30, fill=GREEN)
        cv.create_rectangle(self.ship - 3, HEIGHT - 30, self.ship + 3,
                            HEIGHT - 26, fill=GREEN)
        for a in self.aliens:
            c = COLORS[a["row"] % 4]
            x, y = a["x"], a["y"]
            cv.create_rectangle(x, y, x + AW, y + AH, outline=c)
            cv.create_rectangle(x + 6, y + 8, x + 10, y + 12, fill=c, outline=c)
            cv.create_rectangle(x + AW - 10, y + 8, x + AW - 6, y + 12,
                                fill=c, outline=c)
            cv.create_rectangle(x + 10, y + AH - 6, x + 22, y + AH - 2,
                                fill=c, outline=c)
        for b in self.pb:
            cv.create_rectangle(b[0], b[1], b[0] + 4, b[1] + 10, fill=WHITE)
        for b in self.ab:
            cv.create_rectangle(b[0], b[1], b[0] + 4, b[1] + 10, fill=RED)
        cv.create_text(10, 8, anchor="nw", text="Score: %d" % self.score,
                       fill=WHITE, font=("Helvetica", 14))
        cv.create_text(WIDTH - 10, 8, anchor="ne", text="Lives: %d" % self.lives,
                       fill=GREEN, font=("Helvetica", 14))
        if self.state == "over":
            cv.create_text(WIDTH // 2, HEIGHT // 2 - 20, text="GAME OVER",
                           fill=RED, font=("Helvetica", 32, "bold"))
            cv.create_text(WIDTH // 2, HEIGHT // 2 + 30,
                           text="Final Score: %d  -  Press R to restart" % self.score,
                           fill=WHITE, font=("Helvetica", 12))
        elif self.state == "win":
            cv.create_text(WIDTH // 2, HEIGHT // 2 - 20, text="YOU WIN!",
                           fill=GREEN, font=("Helvetica", 32, "bold"))
            cv.create_text(WIDTH // 2, HEIGHT // 2 + 30,
                           text="Score: %d  -  Press R to play again" % self.score,
                           fill=WHITE, font=("Helvetica", 12))


def main():
    root = tk.Tk()
    Game(root)
    root.mainloop()


if __name__ == "__main__":
    main()