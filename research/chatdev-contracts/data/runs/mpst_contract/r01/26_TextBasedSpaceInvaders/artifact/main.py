import random
import tkinter as tk

W, H = 640, 720
ROWS, COLS = 4, 8
AW, AH = 36, 24
AGAPX, AGAPY = 16, 14
ATOP = 80
GREEN, WHITE, RED, BG = "#50dc50", "#f0f0f0", "#e65050", "#0a0a19"
COLORS = ["#e65050", "#fadc50", "#5a8cff", "#aa5af0"]


def hit(ax, ay, aw, ah, bx, by, bw, bh):
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah


class Game:
    def __init__(self, root):
        self.root = root
        root.title("Space Invaders")
        root.resizable(False, False)
        self.cv = tk.Canvas(root, width=W, height=H, bg=BG, highlightthickness=0)
        self.cv.pack()
        root.bind("<KeyPress>", self.press)
        root.bind("<KeyRelease>", self.release)
        self.keys = set()
        self.reset()
        self.tick()

    def reset(self):
        self.player = [W // 2 - 23, H - 60]
        self.lives, self.score = 3, 0
        self.dir, self.step_timer, self.cooldown = 1, 0, 0
        self.bullets, self.bombs, self.aliens = [], [], []
        for r in range(ROWS):
            for c in range(COLS):
                self.aliens.append([40 + c * (AW + AGAPX), ATOP + r * (AH + AGAPY), r, True])
        self.state = "play"

    def press(self, e):
        k = e.keysym.lower()
        if k == "space" and self.state == "play" and self.cooldown <= 0:
            self.bullets.append([self.player[0] + 21, self.player[1] - 14])
            self.cooldown = 18
        elif self.state != "play":
            if k == "r":
                self.reset()
            elif k == "q":
                self.root.destroy()
                return
        self.keys.add(k)

    def release(self, e):
        self.keys.discard(e.keysym.lower())

    def tick(self):
        if self.state == "play":
            self.update()
        self.draw()
        self.root.after(16, self.tick)

    def update(self):
        if "left" in self.keys or "a" in self.keys:
            self.player[0] -= 5
        if "right" in self.keys or "d" in self.keys:
            self.player[0] += 5
        self.player[0] = max(0, min(W - 46, self.player[0]))
        if self.cooldown > 0:
            self.cooldown -= 1

        self.step_timer += 1
        if self.step_timer >= max(6, 40 - self.score // 20):
            self.step_timer = 0
            xs = [a[0] for a in self.aliens if a[3]]
            if xs:
                step = 8
                if (self.dir > 0 and max(xs) + AW + step >= W) or (self.dir < 0 and min(xs) - step <= 0):
                    self.dir *= -1
                    for a in self.aliens:
                        if a[3]:
                            a[1] += 16
                else:
                    for a in self.aliens:
                        if a[3]:
                            a[0] += self.dir * step
                live = [a for a in self.aliens if a[3]]
                if live and random.random() < 0.4:
                    s = random.choice(live)
                    self.bombs.append([s[0] + AW // 2 - 2, s[1] + AH])

        for b in self.bullets[:]:
            b[1] -= 8
            if b[1] < -12:
                self.bullets.remove(b)
                continue
            for a in self.aliens:
                if a[3] and hit(a[0], a[1], AW, AH, b[0], b[1], 4, 12):
                    a[3] = False
                    self.score += 10 * (ROWS - a[2])
                    self.bullets.remove(b)
                    break

        for b in self.bombs[:]:
            b[1] += 4
            if b[1] > H:
                self.bombs.remove(b)
                continue
            if hit(self.player[0], self.player[1], 46, 22, b[0], b[1], 4, 12):
                self.bombs.remove(b)
                self.lives -= 1
                if self.lives <= 0:
                    self.state = "over"

        for a in self.aliens:
            if a[3] and a[1] + AH >= self.player[1]:
                self.state = "over"
        if self.state == "play" and not any(a[3] for a in self.aliens):
            self.state = "win"

    def draw(self):
        cv = self.cv
        cv.delete("all")
        px, py = self.player
        cv.create_polygon(px + 23, py - 6, px, py + 22, px + 46, py + 22, fill=GREEN)
        cv.create_rectangle(px + 20, py - 14, px + 26, py - 4, fill=GREEN)
        for a in self.aliens:
            if not a[3]:
                continue
            x, y = a[0], a[1]
            c = COLORS[a[2] % len(COLORS)]
            cv.create_rectangle(x + 6, y, x + AW - 6, y + AH, fill=c, outline=c)
            cv.create_rectangle(x, y + 6, x + AW, y + AH - 6, fill=c, outline=c)
            cv.create_rectangle(x + 8, y + 8, x + 14, y + 14, fill=BG, outline=BG)
            cv.create_rectangle(x + AW - 14, y + 8, x + AW - 8, y + 14, fill=BG, outline=BG)
        for b in self.bullets:
            cv.create_rectangle(b[0], b[1], b[0] + 4, b[1] + 12, fill=WHITE)
        for b in self.bombs:
            cv.create_rectangle(b[0], b[1], b[0] + 4, b[1] + 12, fill=RED)
        cv.create_rectangle(0, H - 24, W, H - 20, fill=GREEN)
        cv.create_text(10, 10, anchor="nw", text="Score: %d   Lives: %d" % (self.score, self.lives),
                       fill=WHITE, font=("Helvetica", 14))
        if self.state != "play":
            msg, col = ("GAME OVER", RED) if self.state == "over" else ("YOU WIN!", GREEN)
            cv.create_text(W // 2, H // 2 - 20, text=msg, fill=col, font=("Helvetica", 36, "bold"))
            cv.create_text(W // 2, H // 2 + 30, text="Press R to restart, Q to quit",
                           fill=WHITE, font=("Helvetica", 14))


def main():
    root = tk.Tk()
    Game(root)
    root.mainloop()


if __name__ == "__main__":
    main()