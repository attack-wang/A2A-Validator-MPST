# Two-Player Pong (standard library only -- tkinter GUI, no external dependencies)
import random
import tkinter as tk

WIDTH, HEIGHT = 800, 600
PADDLE_W, PADDLE_H = 12, 100
PADDLE_MARGIN = 10
BALL_SIZE = 14
PADDLE_SPEED = 7
BALL_SPEED_X = 5
BALL_SPEED_Y = 4
MAX_BALL_SPEED = 12
MAX_VY = 10
WINNING_SCORE = 5
FRAME_MS = 16

WHITE, BLACK = "#ffffff", "#000000"


class Pong:
    def __init__(self, root):
        self.root = root
        root.title("Two-Player Pong")
        root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BLACK, highlightthickness=0)
        self.canvas.pack()
        self.keys = set()
        root.bind("<KeyPress>", self._key_down)
        root.bind("<KeyRelease>", self._key_up)
        self.left_score = self.right_score = 0
        self.winner = None
        self.left_y = self.right_y = HEIGHT // 2 - PADDLE_H // 2
        self.reset_ball(random.choice((-1, 1)))
        self._loop()

    def _key_down(self, event):
        key = event.keysym
        if key.lower() == "r" and self.winner is not None:
            self.left_score = self.right_score = 0
            self.winner = None
            self.left_y = self.right_y = HEIGHT // 2 - PADDLE_H // 2
            self.reset_ball(random.choice((-1, 1)))
        self.keys.add(key)

    def _key_up(self, event):
        self.keys.discard(event.keysym)

    def reset_ball(self, direction):
        """Center the ball and serve it horizontally in the given direction (-1 or 1)."""
        self.ball = [WIDTH / 2 - BALL_SIZE / 2, HEIGHT / 2 - BALL_SIZE / 2,
                     BALL_SPEED_X * direction, random.choice((-1, 1)) * BALL_SPEED_Y]

    @staticmethod
    def _clamp(value, low, high):
        return max(low, min(high, value))

    def _loop(self):
        self._update()
        self._draw()
        self.root.after(FRAME_MS, self._loop)

    def _update(self):
        if self.winner is not None:
            return
        keys = self.keys
        if "w" in keys or "W" in keys:
            self.left_y -= PADDLE_SPEED
        if "s" in keys or "S" in keys:
            self.left_y += PADDLE_SPEED
        if "Up" in keys:
            self.right_y -= PADDLE_SPEED
        if "Down" in keys:
            self.right_y += PADDLE_SPEED
        self.left_y = self._clamp(self.left_y, 0, HEIGHT - PADDLE_H)
        self.right_y = self._clamp(self.right_y, 0, HEIGHT - PADDLE_H)

        x, y, vx, vy = self.ball
        x += vx
        y += vy

        # Bounce off top and bottom edges
        if y <= 0 or y >= HEIGHT - BALL_SIZE:
            vy = -vy
            y = self._clamp(y, 0, HEIGHT - BALL_SIZE)

        left = (PADDLE_MARGIN, self.left_y, PADDLE_MARGIN + PADDLE_W, self.left_y + PADDLE_H)
        rx = WIDTH - PADDLE_MARGIN - PADDLE_W
        right = (rx, self.right_y, rx + PADDLE_W, self.right_y + PADDLE_H)

        # Paddle collisions with angle-based spin and slight speed-up
        if vx < 0 and x < left[2] and x + BALL_SIZE > left[0] and y < left[3] and y + BALL_SIZE > left[1]:
            vx = min(abs(vx) * 1.05, MAX_BALL_SPEED)
            offset = (y + BALL_SIZE / 2) - (self.left_y + PADDLE_H / 2)
            vy = self._clamp(vy + offset / (PADDLE_H / 2) * 2, -MAX_VY, MAX_VY)
            x = left[2]
        elif vx > 0 and x + BALL_SIZE > right[0] and x < right[2] and y < right[3] and y + BALL_SIZE > right[1]:
            vx = -min(abs(vx) * 1.05, MAX_BALL_SPEED)
            offset = (y + BALL_SIZE / 2) - (self.right_y + PADDLE_H / 2)
            vy = self._clamp(vy + offset / (PADDLE_H / 2) * 2, -MAX_VY, MAX_VY)
            x = right[0] - BALL_SIZE

        # Scoring: opponent missed, point awarded, ball reset toward the player who missed
        if x + BALL_SIZE < 0:
            self.right_score += 1
            self._set_winner()
            self.reset_ball(-1)
        elif x > WIDTH:
            self.left_score += 1
            self._set_winner()
            self.reset_ball(1)
        else:
            self.ball = [x, y, vx, vy]

    def _set_winner(self):
        if self.left_score >= WINNING_SCORE:
            self.winner = "Left Player (W/S)"
        elif self.right_score >= WINNING_SCORE:
            self.winner = "Right Player (Up/Down)"

    def _draw(self):
        c = self.canvas
        c.delete("all")
        c.create_rectangle(PADDLE_MARGIN, self.left_y, PADDLE_MARGIN + PADDLE_W,
                           self.left_y + PADDLE_H, fill=WHITE, width=0)
        rx = WIDTH - PADDLE_MARGIN - PADDLE_W
        c.create_rectangle(rx, self.right_y, rx + PADDLE_W, self.right_y + PADDLE_H,
                           fill=WHITE, width=0)
        c.create_rectangle(self.ball[0], self.ball[1], self.ball[0] + BALL_SIZE,
                           self.ball[1] + BALL_SIZE, fill=WHITE, width=0)
        c.create_line(WIDTH / 2, 0, WIDTH / 2, HEIGHT, fill=WHITE, dash=(4, 8))
        c.create_text(WIDTH / 2 - 70, 35, text=str(self.left_score), fill=WHITE,
                      font=("Helvetica", 32, "bold"))
        c.create_text(WIDTH / 2 + 70, 35, text=str(self.right_score), fill=WHITE,
                      font=("Helvetica", 32, "bold"))
        c.create_text(WIDTH / 2, HEIGHT - 20,
                      text="Left: W/S    Right: Up/Down    First to {} wins".format(WINNING_SCORE),
                      fill=WHITE, font=("Helvetica", 12))
        if self.winner is not None:
            c.create_text(WIDTH / 2, HEIGHT / 2,
                          text="{} wins!  Press R to restart".format(self.winner),
                          fill=WHITE, font=("Helvetica", 22, "bold"))


def main():
    root = tk.Tk()
    Pong(root)
    root.mainloop()


if __name__ == "__main__":
    main()