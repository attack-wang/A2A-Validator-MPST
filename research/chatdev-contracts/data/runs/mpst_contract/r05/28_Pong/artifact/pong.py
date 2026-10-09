import random
import tkinter as tk

WIDTH, HEIGHT = 800, 600
FPS_MS = 16
PADDLE_W, PADDLE_H = 12, 90
PADDLE_SPEED = 7
BALL_SIZE = 14
BALL_SPEED = 6
MAX_BALL_SPEED = 14
SPEEDUP = 1.05
WIN_SCORE = 5
SERVE_FRAMES = 60
WHITE, BLACK = "#ffffff", "#141414"


class Paddle:
    def __init__(self, canvas, x):
        self.canvas = canvas
        top = (HEIGHT - PADDLE_H) // 2
        self.id = canvas.create_rectangle(x, top, x + PADDLE_W, top + PADDLE_H,
                                          fill=WHITE, outline=WHITE)

    def move(self, direction):
        x1, y1, x2, _ = self.canvas.coords(self.id)
        y1 = max(0.0, min(HEIGHT - PADDLE_H, y1 + direction * PADDLE_SPEED))
        self.canvas.coords(self.id, x1, y1, x2, y1 + PADDLE_H)


class Ball:
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = canvas.create_oval(0, 0, BALL_SIZE, BALL_SIZE,
                                     fill=WHITE, outline=WHITE)
        self.reset()

    def reset(self):
        cx, cy = WIDTH / 2, HEIGHT / 2
        self.canvas.coords(self.id, cx - BALL_SIZE / 2, cy - BALL_SIZE / 2,
                           cx + BALL_SIZE / 2, cy + BALL_SIZE / 2)
        self.vx = BALL_SPEED * random.choice((-1, 1))
        self.vy = random.uniform(-BALL_SPEED, BALL_SPEED)


class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pong - First to %d" % WIN_SCORE)
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT,
                                bg=BLACK, highlightthickness=0)
        self.canvas.pack()
        self.big_font = ("Helvetica", 40, "bold")
        self.font = ("Helvetica", 16)
        self.keys = set()
        for key in ("w", "s", "Up", "Down", "space"):
            self.root.bind("<KeyPress-%s>" % key, self._press)
            self.root.bind("<KeyRelease-%s>" % key, self._release)
        self.root.bind("<Escape>", lambda event: self.stop())
        self.root.protocol("WM_DELETE_WINDOW", self.stop)
        self.running = True
        self.reset_match()
        self.root.after(FPS_MS, self.loop)

    def _press(self, event):
        self.keys.add(event.keysym)

    def _release(self, event):
        self.keys.discard(event.keysym)

    def stop(self):
        self.running = False
        self.root.destroy()

    def reset_match(self):
        self.paddles = [Paddle(self.canvas, 30),
                        Paddle(self.canvas, WIDTH - 30 - PADDLE_W)]
        self.ball = Ball(self.canvas)
        self.scores = [0, 0]
        self.score_ids = [
            self.canvas.create_text(WIDTH // 4, 40, text="0",
                                    fill=WHITE, font=self.big_font),
            self.canvas.create_text(WIDTH * 3 // 4, 40, text="0",
                                    fill=WHITE, font=self.big_font)]
        self.msg_id = self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="",
                                              fill=WHITE, font=self.font)
        self.serve_delay = SERVE_FRAMES
        self.winner = None

    def run(self):
        self.root.mainloop()

    def loop(self):
        if not self.running:
            return
        try:
            self.update()
        except tk.TclError:
            return
        self.root.after(FPS_MS, self.loop)

    def update(self):
        if "w" in self.keys:
            self.paddles[0].move(-1)
        if "s" in self.keys:
            self.paddles[0].move(1)
        if "Up" in self.keys:
            self.paddles[1].move(-1)
        if "Down" in self.keys:
            self.paddles[1].move(1)

        if self.winner is not None:
            self.canvas.itemconfigure(
                self.msg_id,
                text="Player %d wins! Press SPACE for a new match" % (self.winner + 1))
            if "space" in self.keys:
                self.canvas.delete("all")
                self.reset_match()
            return

        if self.serve_delay > 0:
            self.canvas.itemconfigure(self.msg_id, text="Press SPACE to serve")
            if "space" in self.keys:
                self.serve_delay = 0
            else:
                self.serve_delay -= 1
                return
        self.canvas.itemconfigure(self.msg_id, text="")

        ball = self.ball
        x1, y1, x2, y2 = ball.canvas.coords(ball.id)
        x1 += ball.vx
        x2 += ball.vx
        y1 += ball.vy
        y2 += ball.vy
        if y1 <= 0:
            y1, y2 = 0.0, float(BALL_SIZE)
            ball.vy = abs(ball.vy)
        elif y2 >= HEIGHT:
            y1, y2 = float(HEIGHT - BALL_SIZE), float(HEIGHT)
            ball.vy = -abs(ball.vy)
        ball.canvas.coords(ball.id, x1, y1, x2, y2)

        for i, paddle in enumerate(self.paddles):
            px1, py1, px2, py2 = paddle.canvas.coords(paddle.id)
            if x2 > px1 and x1 < px2 and y2 > py1 and y1 < py2 and (
                    (i == 0 and ball.vx < 0) or (i == 1 and ball.vx > 0)):
                offset = (y1 + y2) / 2 - (py1 + py2) / 2
                offset = max(-1.0, min(1.0, offset / (PADDLE_H / 2)))
                speed = min(abs(ball.vx) * SPEEDUP, MAX_BALL_SPEED)
                ball.vx = speed if i == 0 else -speed
                ball.vy = offset * speed * 0.9
                if i == 0:
                    x1, x2 = px2, px2 + BALL_SIZE
                else:
                    x1, x2 = px1 - BALL_SIZE, px1
                ball.canvas.coords(ball.id, x1, y1, x2, y2)

        if x2 < 0:
            self.award_point(1)
        elif x1 > WIDTH:
            self.award_point(0)

    def award_point(self, player):
        self.scores[player] += 1
        self.canvas.itemconfigure(self.score_ids[player],
                                  text=str(self.scores[player]))
        if self.scores[player] >= WIN_SCORE:
            self.winner = player
        else:
            self.ball.reset()
            self.serve_delay = SERVE_FRAMES