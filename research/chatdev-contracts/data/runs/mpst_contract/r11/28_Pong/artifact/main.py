import random
import tkinter as tk

WIDTH, HEIGHT = 800, 600
PADDLE_W, PADDLE_H = 12, 90
PADDLE_SPEED = 7
BALL_SIZE = 12
BASE_SPEED = 6.0
MAX_SPEED = 13.0
MAX_VY = 5.5
WIN_SCORE = 7
FG, BG = "#f0f0f0", "#0f0f0f"
LX = 30
RX = WIDTH - 30 - PADDLE_W


class Game:
    def __init__(self, root):
        self.root = root
        root.title("Pong - P1: W/S   P2: Up/Down   First to %d" % WIN_SCORE)
        root.resizable(False, False)
        self.cv = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG, highlightthickness=0)
        self.cv.pack()
        self.keys = set()
        for k in ("w", "s", "Up", "Down"):
            root.bind("<KeyPress-%s>" % k, lambda e, k=k: self.keys.add(k))
            root.bind("<KeyRelease-%s>" % k, lambda e, k=k: self.keys.discard(k))
        root.bind("<KeyPress-r>", self.restart)
        root.bind("<KeyPress-R>", self.restart)
        y = 0
        while y < HEIGHT:
            self.cv.create_rectangle(WIDTH // 2 - 1, y, WIDTH // 2 + 1, y + 14, fill=FG, width=0)
            y += 24
        self.score_id = self.cv.create_text(WIDTH // 2, 45, text="", fill=FG,
                                            font=("Helvetica", 34, "bold"))
        self.lid = self.cv.create_rectangle(0, 0, 0, 0, fill=FG, width=0)
        self.rid = self.cv.create_rectangle(0, 0, 0, 0, fill=FG, width=0)
        self.bid = self.cv.create_rectangle(0, 0, 0, 0, fill=FG, width=0)
        self.msg_ids = []
        self.scores = [0, 0]
        self.game_over = False
        self.ly = self.ry = (HEIGHT - PADDLE_H) // 2
        self.reset_ball(random.choice((-1, 1)))
        self.tick()

    def reset_ball(self, direction):
        self.bx = (WIDTH - BALL_SIZE) / 2.0
        self.by = (HEIGHT - BALL_SIZE) / 2.0
        self.vx = direction * BASE_SPEED
        self.vy = random.choice((-1, 1)) * random.uniform(1.5, MAX_VY)

    def bounce(self, center_y, to_right):
        speed = min(abs(self.vx) + 0.4, MAX_SPEED)
        self.vx = speed if to_right else -speed
        offset = (self.by + BALL_SIZE / 2.0 - center_y) / (PADDLE_H / 2.0)
        self.vy = max(-1.0, min(1.0, offset)) * MAX_VY

    def hits(self, px, py):
        return (self.bx < px + PADDLE_W and self.bx + BALL_SIZE > px and
                self.by < py + PADDLE_H and self.by + BALL_SIZE > py)

    def restart(self, event=None):
        if self.game_over:
            for mid in self.msg_ids:
                self.cv.delete(mid)
            self.msg_ids = []
            self.scores = [0, 0]
            self.game_over = False
            self.reset_ball(random.choice((-1, 1)))

    def tick(self):
        if not self.game_over:
            if "w" in self.keys:
                self.ly = max(0, self.ly - PADDLE_SPEED)
            if "s" in self.keys:
                self.ly = min(HEIGHT - PADDLE_H, self.ly + PADDLE_SPEED)
            if "Up" in self.keys:
                self.ry = max(0, self.ry - PADDLE_SPEED)
            if "Down" in self.keys:
                self.ry = min(HEIGHT - PADDLE_H, self.ry + PADDLE_SPEED)

            self.bx += self.vx
            self.by += self.vy
            if self.by <= 0:
                self.by = 0
                self.vy = abs(self.vy)
            elif self.by + BALL_SIZE >= HEIGHT:
                self.by = HEIGHT - BALL_SIZE
                self.vy = -abs(self.vy)
            if self.vx < 0 and self.hits(LX, self.ly):
                self.bx = LX + PADDLE_W
                self.bounce(self.ly + PADDLE_H / 2.0, True)
            elif self.vx > 0 and self.hits(RX, self.ry):
                self.bx = RX - BALL_SIZE
                self.bounce(self.ry + PADDLE_H / 2.0, False)

            if self.bx + BALL_SIZE < 0:
                self.scores[1] += 1
                self.reset_ball(-1)
            elif self.bx > WIDTH:
                self.scores[0] += 1
                self.reset_ball(1)

            if self.scores[0] >= WIN_SCORE or self.scores[1] >= WIN_SCORE:
                self.game_over = True
                winner = "Player 1" if self.scores[0] > self.scores[1] else "Player 2"
                self.msg_ids.append(self.cv.create_text(
                    WIDTH // 2, HEIGHT // 2 - 50, text="%s wins!" % winner,
                    fill=FG, font=("Helvetica", 40, "bold")))
                self.msg_ids.append(self.cv.create_text(
                    WIDTH // 2, HEIGHT // 2 + 10, text="Press R to play again",
                    fill=FG, font=("Helvetica", 22)))

        self.cv.coords(self.lid, LX, self.ly, LX + PADDLE_W, self.ly + PADDLE_H)
        self.cv.coords(self.rid, RX, self.ry, RX + PADDLE_W, self.ry + PADDLE_H)
        self.cv.coords(self.bid, self.bx, self.by, self.bx + BALL_SIZE, self.by + BALL_SIZE)
        self.cv.itemconfig(self.score_id, text="%d    %d" % (self.scores[0], self.scores[1]))
        self.root.after(16, self.tick)


def main():
    root = tk.Tk()
    Game(root)
    root.mainloop()


if __name__ == "__main__":
    main()