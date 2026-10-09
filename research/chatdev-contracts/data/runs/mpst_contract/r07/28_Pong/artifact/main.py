import random
import tkinter as tk

W, H = 800, 480
PW, PH = 12, 80
BR = 6
SPEED = 6
WIN_SCORE = 7
P1X, P2X = 30, W - 30 - PW


class Pong:
    def __init__(self, root):
        self.root = root
        root.title("Two-Player Pong")
        self.cv = tk.Canvas(root, width=W, height=H, bg="#141414", highlightthickness=0)
        self.cv.pack()
        for y in range(0, H, 24):
            self.cv.create_rectangle(W // 2 - 2, y, W // 2 + 2, y + 12, fill="#555555", width=0)
        self.p1 = self.cv.create_rectangle(P1X, 0, P1X + PW, PH, fill="white", width=0)
        self.p2 = self.cv.create_rectangle(P2X, 0, P2X + PW, PH, fill="white", width=0)
        self.ball = self.cv.create_oval(0, 0, 0, 0, fill="white", width=0)
        self.s1 = self.cv.create_text(W // 2 - 60, 32, text="0", fill="white", font=("Helvetica", 32, "bold"))
        self.s2 = self.cv.create_text(W // 2 + 60, 32, text="0", fill="white", font=("Helvetica", 32, "bold"))
        self.msg = self.cv.create_text(W // 2, H // 2, text="", fill="white", font=("Helvetica", 26, "bold"))
        self.keys = set()
        root.bind("<KeyPress>", self.key_down)
        root.bind("<KeyRelease>", self.key_up)
        self.reset()
        self.tick()

    def key_down(self, e):
        k = e.keysym.lower()
        self.keys.add(k)
        if k == "r" and self.winner is not None:
            self.reset()

    def key_up(self, e):
        self.keys.discard(e.keysym.lower())

    def reset(self):
        self.p1y = self.p2y = (H - PH) / 2.0
        self.scores = [0, 0]
        self.winner = None
        self.serve(random.choice([-1, 1]))
        self.cv.itemconfig(self.msg, text="")

    def serve(self, d):
        self.bx, self.by = W / 2.0, H / 2.0
        self.bvx, self.bvy = SPEED * d, random.choice([-4, -3, 3, 4])

    def move(self, y, up, dn):
        if up in self.keys:
            y -= SPEED
        if dn in self.keys:
            y += SPEED
        return max(0.0, min(H - PH, y))

    def tick(self):
        if self.winner is None:
            self.p1y = self.move(self.p1y, "w", "s")
            self.p2y = self.move(self.p2y, "up", "down")
            self.bx += self.bvx
            self.by += self.bvy
            if self.by - BR <= 0 or self.by + BR >= H:
                self.bvy *= -1
                self.by = max(BR, min(H - BR, self.by))
            if self.bvx < 0 and self.bx - BR <= P1X + PW and self.bx > P1X and \
                    self.p1y - BR <= self.by <= self.p1y + PH + BR:
                self.bvx = min(abs(self.bvx) * 1.05, 14)
                self.bvy = max(-10, min(10, self.bvy + (self.by - (self.p1y + PH / 2)) * 0.08))
                self.bx = P1X + PW + BR
            if self.bvx > 0 and self.bx + BR >= P2X and self.bx < P2X + PW and \
                    self.p2y - BR <= self.by <= self.p2y + PH + BR:
                self.bvx = -min(abs(self.bvx) * 1.05, 14)
                self.bvy = max(-10, min(10, self.bvy + (self.by - (self.p2y + PH / 2)) * 0.08))
                self.bx = P2X - BR
            if self.bx + BR < 0:
                self.scores[1] += 1
                self.serve(-1)
            elif self.bx - BR > W:
                self.scores[0] += 1
                self.serve(1)
            if self.scores[0] >= WIN_SCORE or self.scores[1] >= WIN_SCORE:
                self.winner = 0 if self.scores[0] >= WIN_SCORE else 1
                self.cv.itemconfig(self.msg, text="Player %d wins!  R = restart" % (self.winner + 1))
            self.cv.itemconfig(self.s1, text=str(self.scores[0]))
            self.cv.itemconfig(self.s2, text=str(self.scores[1]))
        self.cv.coords(self.p1, P1X, self.p1y, P1X + PW, self.p1y + PH)
        self.cv.coords(self.p2, P2X, self.p2y, P2X + PW, self.p2y + PH)
        self.cv.coords(self.ball, self.bx - BR, self.by - BR, self.bx + BR, self.by + BR)
        self.root.after(16, self.tick)


if __name__ == "__main__":
    root = tk.Tk()
    Pong(root)
    root.mainloop()