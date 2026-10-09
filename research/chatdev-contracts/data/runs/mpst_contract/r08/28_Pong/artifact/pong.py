import random
import tkinter as tk

WIDTH, HEIGHT = 800, 600
PADDLE_W, PADDLE_H = 12, 100
PADDLE_MARGIN = 30
BALL_SIZE = 14
PADDLE_SPEED = 7
BALL_SPEED = 6
MAX_BALL_SPEED = 12
WINNING_SCORE = 5
TICK = 16

BG, FG = "#000000", "#ffffff"


class PongGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Two-Player Pong")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT,
                                bg=BG, highlightthickness=0)
        self.canvas.pack()
        self.root.bind("<KeyPress>", self._key_down)
        self.root.bind("<KeyRelease>", self._key_up)
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.keys = set()
        self.running = True
        self.reset_game()
        self.loop()

    def reset_game(self):
        self.left_y = HEIGHT // 2 - PADDLE_H // 2
        self.right_y = self.left_y
        self.left_score = 0
        self.right_score = 0
        self.message = None
        self.reset_ball(random.choice([-1, 1]))

    def reset_ball(self, direction):
        self.ball_x = WIDTH / 2 - BALL_SIZE / 2
        self.ball_y = HEIGHT / 2 - BALL_SIZE / 2
        self.ball_vx = BALL_SPEED * direction
        self.ball_vy = random.choice([-1, 1]) * random.uniform(1.5, 4.5)

    def _key_down(self, event):
        key = event.keysym.lower()
        if key == "q":
            self.quit()
            return
        if self.message and key == "r":
            self.reset_game()
            return
        self.keys.add(key)

    def _key_up(self, event):
        self.keys.discard(event.keysym.lower())

    def quit(self):
        self.running = False
        self.root.destroy()

    def move_paddles(self):
        if "w" in self.keys:
            self.left_y = max(0, self.left_y - PADDLE_SPEED)
        if "s" in self.keys:
            self.left_y = min(HEIGHT - PADDLE_H, self.left_y + PADDLE_SPEED)
        if "up" in self.keys:
            self.right_y = max(0, self.right_y - PADDLE_SPEED)
        if "down" in self.keys:
            self.right_y = min(HEIGHT - PADDLE_H, self.right_y + PADDLE_SPEED)

    def step_ball(self):
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy
        if self.ball_y <= 0:
            self.ball_y = 0
            self.ball_vy = abs(self.ball_vy)
        elif self.ball_y + BALL_SIZE >= HEIGHT:
            self.ball_y = HEIGHT - BALL_SIZE
            self.ball_vy = -abs(self.ball_vy)
        self.check_paddles()
        self.check_score()

    def hits(self, paddle_y, paddle_x):
        return (self.ball_y + BALL_SIZE >= paddle_y and
                self.ball_y <= paddle_y + PADDLE_H and
                self.ball_x <= paddle_x + PADDLE_W and
                self.ball_x + BALL_SIZE >= paddle_x)

    def check_paddles(self):
        if self.ball_vx < 0 and self.hits(self.left_y, PADDLE_MARGIN):
            self.ball_x = PADDLE_MARGIN + PADDLE_W
            self.bounce(self.left_y)
        elif self.ball_vx > 0 and self.hits(self.right_y,
                                            WIDTH - PADDLE_MARGIN - PADDLE_W):
            self.ball_x = WIDTH - PADDLE_MARGIN - PADDLE_W - BALL_SIZE
            self.bounce(self.right_y)

    def bounce(self, paddle_y):
        speed = min(abs(self.ball_vx) + 0.4, MAX_BALL_SPEED)
        rel = (self.ball_y + BALL_SIZE / 2 - (paddle_y + PADDLE_H / 2)) / (PADDLE_H / 2)
        self.ball_vx = speed if self.ball_vx < 0 else -speed
        self.ball_vy = max(-6.0, min(6.0, rel * BALL_SPEED))

    def check_score(self):
        scorer = None
        if self.ball_x + BALL_SIZE < 0:
            self.right_score += 1
            scorer = "right"
        elif self.ball_x > WIDTH:
            self.left_score += 1
            scorer = "left"
        if scorer is None:
            return
        score = self.right_score if scorer == "right" else self.left_score
        if score >= WINNING_SCORE:
            winner = "Player 1 (Left)" if scorer == "left" else "Player 2 (Right)"
            self.message = f"{winner} wins! Press R to restart, Q to quit"
        else:
            self.reset_ball(-1 if scorer == "right" else 1)

    def draw(self):
        c = self.canvas
        c.delete("all")
        c.create_line(WIDTH // 2, 0, WIDTH // 2, HEIGHT, fill=FG, dash=(4, 8))
        c.create_rectangle(PADDLE_MARGIN, self.left_y, PADDLE_MARGIN + PADDLE_W,
                           self.left_y + PADDLE_H, fill=FG)
        rx = WIDTH - PADDLE_MARGIN - PADDLE_W
        c.create_rectangle(rx, self.right_y, rx + PADDLE_W,
                           self.right_y + PADDLE_H, fill=FG)
        c.create_rectangle(self.ball_x, self.ball_y, self.ball_x + BALL_SIZE,
                           self.ball_y + BALL_SIZE, fill=FG)
        c.create_text(WIDTH // 4, 40, text=str(self.left_score), fill=FG,
                      font=("Consolas", 40, "bold"))
        c.create_text(WIDTH * 3 // 4, 40, text=str(self.right_score), fill=FG,
                      font=("Consolas", 40, "bold"))
        c.create_text(WIDTH // 2, HEIGHT - 20,
                      text=f"Left: W/S    Right: Up/Down    First to {WINNING_SCORE} wins",
                      fill=FG, font=("Consolas", 14))
        if self.message:
            c.create_text(WIDTH // 2, HEIGHT // 2, text=self.message, fill=FG,
                          font=("Consolas", 16, "bold"))

    def loop(self):
        if not self.running:
            return
        if self.message is None:
            self.move_paddles()
            self.step_ball()
        self.draw()
        self.root.after(TICK, self.loop)

    def run(self):
        self.root.mainloop()