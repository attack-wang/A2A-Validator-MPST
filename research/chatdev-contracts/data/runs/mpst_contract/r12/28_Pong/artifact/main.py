import random
import tkinter as tk

WIDTH, HEIGHT = 800, 600
TICK_MS = 16
WHITE, BLACK = "#ffffff", "#0f0f0f"
PADDLE_W, PADDLE_H, PADDLE_SPEED = 12, 90, 7
BALL_SIZE, BALL_SPEED, SPEED_UP, MAX_SPEED = 14, 6, 0.5, 14
WIN_SCORE = 5
SERVE_DELAY = 45


class Game:
    def __init__(self, root):
        self.root = root
        self.cv = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BLACK, highlightthickness=0)
        self.cv.pack()
        self.big = ("Helvetica", 44, "bold")
        self.small = ("Helvetica", 14)
        self.keys = set()
        root.bind("<KeyPress>", self.on_key)
        root.bind("<KeyRelease>", self.off_key)
        self.score = [0, 0]
        self.p1 = [30, (HEIGHT - PADDLE_H) // 2]
        self.p2 = [WIDTH - 30 - PADDLE_W, (HEIGHT - PADDLE_H) // 2]
        self.ball = [0.0, 0.0]
        self.vx = self.vy = 0.0
        self.delay = 0
        self.over = False
        self.msg = ""
        self.reset_ball(random.choice((-1, 1)))
        self.tick()

    def on_key(self, event):
        key = event.keysym
        if key == "Escape":
            self.root.destroy()
            return
        if self.over and key.lower() == "r":
            self.score = [0, 0]
            self.over = False
            self.msg = ""
            self.reset_ball(random.choice((-1, 1)))
        self.keys.add(key)
        self.keys.add(key.lower())

    def off_key(self, event):
        self.keys.discard(event.keysym)
        self.keys.discard(event.keysym.lower())

    def reset_ball(self, direction):
        self.ball = [WIDTH / 2 - BALL_SIZE / 2, HEIGHT / 2 - BALL_SIZE / 2]
        self.vx = direction * BALL_SPEED
        self.vy = random.uniform(-0.7, 0.7) * BALL_SPEED
        self.delay = SERVE_DELAY

    def move_paddle(self, paddle, dy):
        paddle[1] = max(0, min(HEIGHT - PADDLE_H, paddle[1] + dy))

    def tick(self):
        if not self.over:
            if "w" in self.keys:
                self.move_paddle(self.p1, -PADDLE_SPEED)
            if "s" in self.keys:
                self.move_paddle(self.p1, PADDLE_SPEED)
            if "Up" in self.keys:
                self.move_paddle(self.p2, -PADDLE_SPEED)
            if "Down" in self.keys:
                self.move_paddle(self.p2, PADDLE_SPEED)
            if self.delay > 0:
                self.delay -= 1
            else:
                self.step_ball()
        self.render()
        self.root.after(TICK_MS, self.tick)

    def step_ball(self):
        self.ball[0] += self.vx
        self.ball[1] += self.vy
        if self.ball[1] <= 0:
            self.ball[1] = 0
            self.vy = abs(self.vy)
        elif self.ball[1] >= HEIGHT - BALL_SIZE:
            self.ball[1] = HEIGHT - BALL_SIZE
            self.vy = -abs(self.vy)
        x, y = self.ball
        if (self.vx < 0 and x <= self.p1[0] + PADDLE_W and x + BALL_SIZE >= self.p1[0]
                and y + BALL_SIZE >= self.p1[1] and y <= self.p1[1] + PADDLE_H):
            self.ball[0] = self.p1[0] + PADDLE_W
            self.vx = min(abs(self.vx) + SPEED_UP, MAX_SPEED)
            self.vy = (y + BALL_SIZE / 2 - (self.p1[1] + PADDLE_H / 2)) / (PADDLE_H / 2) * BALL_SPEED
        elif (self.vx > 0 and x + BALL_SIZE >= self.p2[0] and x <= self.p2[0] + PADDLE_W
                and y + BALL_SIZE >= self.p2[1] and y <= self.p2[1] + PADDLE_H):
            self.ball[0] = self.p2[0] - BALL_SIZE
            self.vx = -min(abs(self.vx) + SPEED_UP, MAX_SPEED)
            self.vy = (y + BALL_SIZE / 2 - (self.p2[1] + PADDLE_H / 2)) / (PADDLE_H / 2) * BALL_SPEED
        if self.ball[0] + BALL_SIZE < 0:
            self.score[1] += 1
            self.check_win()
            self.reset_ball(-1)
        elif self.ball[0] > WIDTH:
            self.score[0] += 1
            self.check_win()
            self.reset_ball(1)

    def check_win(self):
        if self.score[0] >= WIN_SCORE or self.score[1] >= WIN_SCORE:
            self.over = True
            self.msg = "Player 1 wins!" if self.score[0] >= WIN_SCORE else "Player 2 wins!"

    def render(self):
        cv = self.cv
        cv.delete("all")
        for y in range(10, HEIGHT, 30):
            cv.create_rectangle(WIDTH // 2 - 2, y, WIDTH // 2 + 2, y + 16, fill=WHITE, outline="")
        cv.create_text(WIDTH // 4, 50, text=str(self.score[0]), fill=WHITE, font=self.big)
        cv.create_text(3 * WIDTH // 4, 50, text=str(self.score[1]), fill=WHITE, font=self.big)
        cv.create_rectangle(self.p1[0], self.p1[1], self.p1[0] + PADDLE_W,
                            self.p1[1] + PADDLE_H, fill=WHITE, outline="")
        cv.create_rectangle(self.p2[0], self.p2[1], self.p2[0] + PADDLE_W,
                            self.p2[1] + PADDLE_H, fill=WHITE, outline="")
        cv.create_rectangle(self.ball[0], self.ball[1], self.ball[0] + BALL_SIZE,
                            self.ball[1] + BALL_SIZE, fill=WHITE, outline="")
        if self.over:
            cv.create_text(WIDTH // 2, HEIGHT // 2 - 60, text=self.msg, fill=WHITE, font=self.big)
            cv.create_text(WIDTH // 2, HEIGHT // 2, text=f"{self.score[0]} - {self.score[1]}",
                           fill=WHITE, font=self.big)
            cv.create_text(WIDTH // 2, HEIGHT // 2 + 70, text="Press R to play again, ESC to quit",
                           fill=WHITE, font=self.small)
        elif self.delay > 0:
            cv.create_text(WIDTH // 2, HEIGHT - 40, text="Get ready...", fill=WHITE, font=self.small)


def main():
    root = tk.Tk()
    root.title("Pong  |  P1: W/S   P2: Arrow Up/Down")
    root.resizable(False, False)
    Game(root)
    root.mainloop()


if __name__ == "__main__":
    main()