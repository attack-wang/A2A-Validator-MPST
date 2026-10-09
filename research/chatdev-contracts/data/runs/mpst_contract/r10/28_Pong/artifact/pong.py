import random
import tkinter as tk

WIDTH, HEIGHT = 800, 500
FPS = 60
PADDLE_W, PADDLE_H = 12, 90
PADDLE_SPEED = 6
BALL_SIZE = 12
BALL_SPEED = 6
MAX_BALL_SPEED = 14
WIN_SCORE = 5
WHITE = "#ffffff"
BLACK = "#141414"
ARROW_KEYS = ("Up", "Down", "Left", "Right")


class Paddle:
    def __init__(self, x, up_key, down_key):
        self.x = x
        self.y = HEIGHT // 2 - PADDLE_H // 2
        self.up_key = up_key
        self.down_key = down_key
        self.score = 0

    def move(self, keys):
        if self.up_key in keys and self.y > 0:
            self.y -= PADDLE_SPEED
        if self.down_key in keys and self.y + PADDLE_H < HEIGHT:
            self.y += PADDLE_SPEED

    def reset(self):
        self.y = HEIGHT // 2 - PADDLE_H // 2
        self.score = 0


class Ball:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.vx = 0.0
        self.vy = 0.0

    def reset(self, direction):
        self.x = WIDTH // 2 - BALL_SIZE / 2
        self.y = HEIGHT // 2 - BALL_SIZE / 2
        angle = random.uniform(-0.7, 0.7)
        self.vx = direction * BALL_SPEED
        self.vy = angle * BALL_SPEED

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.y <= 0:
            self.y = 0
            self.vy = abs(self.vy)
        elif self.y + BALL_SIZE >= HEIGHT:
            self.y = HEIGHT - BALL_SIZE
            self.vy = -abs(self.vy)

    def hits(self, px, py):
        return (self.x < px + PADDLE_W and self.x + BALL_SIZE > px and
                self.y < py + PADDLE_H and self.y + BALL_SIZE > py)


class Game:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                                bg=BLACK, highlightthickness=0)
        self.canvas.pack()
        root.bind("<KeyPress>", self._key_down)
        root.bind("<KeyRelease>", self._key_up)
        self.keys = set()
        self.big_font = ("Helvetica", 32, "bold")
        self.font = ("Helvetica", 11)
        self.left = Paddle(30, "w", "s")
        self.right = Paddle(WIDTH - 42, "Up", "Down")
        self.ball = Ball()
        self.serve_dir = random.choice((-1, 1))
        self.ball.reset(self.serve_dir)
        self.state = "serve"
        self.winner = None
        self._create_items()
        self._tick()

    def _create_items(self):
        c = self.canvas
        for y in range(10, HEIGHT, 24):
            c.create_rectangle(WIDTH // 2 - 2, y, WIDTH // 2 + 2, y + 12,
                               fill=WHITE, outline="")
        self.left_item = c.create_rectangle(0, 0, 0, 0, fill=WHITE, outline="")
        self.right_item = c.create_rectangle(0, 0, 0, 0, fill=WHITE, outline="")
        self.ball_item = c.create_oval(0, 0, 0, 0, fill=WHITE, outline="")
        self.left_score = c.create_text(WIDTH // 2 - 70, 40, text="0",
                                        fill=WHITE, font=self.big_font)
        self.right_score = c.create_text(WIDTH // 2 + 70, 40, text="0",
                                         fill=WHITE, font=self.big_font)
        self.message = c.create_text(WIDTH // 2, HEIGHT - 30, text="",
                                     fill=WHITE, font=self.font)

    @staticmethod
    def _normalize(keysym):
        return keysym if keysym in ARROW_KEYS else keysym.lower()

    def _key_down(self, event):
        key = self._normalize(event.keysym)
        if key == "space":
            if "space" not in self.keys:
                if self.state == "serve":
                    self.state = "play"
                elif self.state == "over":
                    self.restart()
                self.keys.add("space")
            return
        self.keys.add(key)

    def _key_up(self, event):
        self.keys.discard(self._normalize(event.keysym))

    def restart(self):
        self.left.reset()
        self.right.reset()
        self.serve_dir = random.choice((-1, 1))
        self.ball.reset(self.serve_dir)
        self.winner = None
        self.state = "serve"

    def update(self):
        self.left.move(self.keys)
        self.right.move(self.keys)
        if self.state == "play":
            self.ball.update()
            self.collide()
            if self.ball.x + BALL_SIZE <= 0:
                self.score_point(self.right)
            elif self.ball.x >= WIDTH:
                self.score_point(self.left)

    def collide(self):
        ball = self.ball
        if ball.vx < 0 and ball.hits(self.left.x, self.left.y):
            self.bounce(self.left, 1)
        elif ball.vx > 0 and ball.hits(self.right.x, self.right.y):
            self.bounce(self.right, -1)

    def bounce(self, paddle, direction):
        ball = self.ball
        offset = (ball.y + BALL_SIZE / 2 - (paddle.y + PADDLE_H / 2)) / (PADDLE_H / 2)
        offset = max(-1.0, min(1.0, offset))
        speed = min(abs(ball.vx) * 1.05 + 0.3, MAX_BALL_SPEED)
        ball.vx = direction * speed
        ball.vy = offset * speed * 0.8
        if direction > 0:
            ball.x = paddle.x + PADDLE_W
        else:
            ball.x = paddle.x - BALL_SIZE

    def score_point(self, scorer):
        scorer.score += 1
        if scorer.score >= WIN_SCORE:
            self.winner = scorer
            self.ball.x = WIDTH // 2 - BALL_SIZE / 2
            self.ball.y = HEIGHT // 2 - BALL_SIZE / 2
            self.state = "over"
        else:
            self.serve_dir = 1 if scorer is self.left else -1
            self.ball.reset(self.serve_dir)
            self.state = "serve"

    def draw(self):
        c = self.canvas
        c.coords(self.left_item, self.left.x, self.left.y,
                 self.left.x + PADDLE_W, self.left.y + PADDLE_H)
        c.coords(self.right_item, self.right.x, self.right.y,
                 self.right.x + PADDLE_W, self.right.y + PADDLE_H)
        c.coords(self.ball_item, self.ball.x, self.ball.y,
                 self.ball.x + BALL_SIZE, self.ball.y + BALL_SIZE)
        c.itemconfigure(self.left_score, text=str(self.left.score))
        c.itemconfigure(self.right_score, text=str(self.right.score))
        if self.state == "serve":
            msg = ("Press SPACE to serve  |  Left: W/S   Right: Up/Down  |  "
                   "First to %d wins" % WIN_SCORE)
        elif self.state == "over":
            num = "1" if self.winner is self.left else "2"
            msg = "Player %s wins!  Press SPACE for a new game" % num
        else:
            msg = ""
        c.itemconfigure(self.message, text=msg)

    def _tick(self):
        self.update()
        self.draw()
        self.canvas.after(1000 // FPS, self._tick)

    def quit(self):
        self.root.destroy()