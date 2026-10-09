import random
import tkinter as tk

W, H = 400, 600
GROUND = 520
GRAV = 0.45
FLAP = -7.5
BIRD_X, R = 80, 12
PIPE_W = 60


class Game:
    def __init__(self, root):
        self.root = root
        root.title("Flappy Bird")
        root.resizable(False, False)
        self.cv = tk.Canvas(root, width=W, height=H, bg="#71c5cf",
                            highlightthickness=0)
        self.cv.pack()
        root.bind("<space>", self.flap)
        root.bind("<Up>", self.flap)
        root.bind("<Escape>", lambda e: root.destroy())
        self.big = ("Helvetica", 28, "bold")
        self.small = ("Helvetica", 14)
        self.reset()
        self.loop()

    def reset(self):
        self.y = H // 2
        self.v = 0.0
        self.pipes = []
        self.score = 0
        self.spawn = 60
        self.over = False
        self.started = False

    def speed(self):
        return min(3.0 + self.score * 0.05, 6.0)

    def gap_size(self):
        return max(180 - self.score * 2, 110)

    def add_pipe(self):
        gap = self.gap_size()
        margin = 60
        top = random.randint(margin, GROUND - gap - margin)
        self.pipes.append({"x": float(W), "top": top, "gap": gap,
                           "passed": False})

    def flap(self, e=None):
        if self.over:
            self.reset()
        else:
            self.started = True
            self.v = FLAP

    def step(self):
        if not (self.started and not self.over):
            return
        self.v += GRAV
        self.y += self.v
        if self.y - R < 0:
            self.y = R
            self.v = 0.0
        sp = self.speed()
        self.spawn -= 1
        if self.spawn <= 0:
            self.add_pipe()
            self.spawn = int(270 / sp)
        for p in self.pipes:
            p["x"] -= sp
        self.pipes = [p for p in self.pipes if p["x"] + PIPE_W > -10]
        for p in self.pipes:
            if not p["passed"] and p["x"] + PIPE_W < BIRD_X - R:
                p["passed"] = True
                self.score += 1
        if self.y + R >= GROUND:
            self.over = True
            return
        for p in self.pipes:
            if BIRD_X + R > p["x"] and BIRD_X - R < p["x"] + PIPE_W:
                if self.y - R < p["top"] or self.y + R > p["top"] + p["gap"]:
                    self.over = True
                    break

    def draw(self):
        cv = self.cv
        cv.delete("all")
        cv.create_rectangle(0, GROUND, W, H, fill="#ded895", outline="")
        for p in self.pipes:
            x = int(p["x"])
            cv.create_rectangle(x, 0, x + PIPE_W, int(p["top"]),
                                fill="#6fc445", outline="")
            cv.create_rectangle(x, int(p["top"] + p["gap"]), x + PIPE_W,
                                GROUND, fill="#6fc445", outline="")
        by = int(self.y)
        cv.create_oval(BIRD_X - R, by - R, BIRD_X + R, by + R,
                       fill="#ffcc00", outline="")
        cv.create_polygon(BIRD_X, by, BIRD_X + 12, by, BIRD_X, by + 6,
                          fill="#ff8c00", outline="")
        cv.create_oval(BIRD_X + 3, by - 6, BIRD_X + 7, by - 2,
                       fill="#1e1e1e", outline="")
        cv.create_text(W // 2, 34, text=str(self.score), fill="white",
                       font=self.big)
        if not self.started:
            cv.create_text(W // 2, H // 2 - 80, text="Press SPACE to flap",
                           fill="white", font=self.small)
        if self.over:
            cv.create_text(W // 2, H // 2 - 30,
                           text="Game Over! SPACE = retry",
                           fill="#ff4646", font=self.big)

    def loop(self):
        self.step()
        self.draw()
        self.root.after(16, self.loop)


def main():
    root = tk.Tk()
    Game(root)
    root.mainloop()


if __name__ == "__main__":
    main()