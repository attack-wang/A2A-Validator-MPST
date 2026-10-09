import random
import tkinter as tk

WIDTH, HEIGHT = 800, 500
PADDLE_W, PADDLE_H = 12, 90
PADDLE_MARGIN = 20
BALL_SIZE = 12
PADDLE_SPEED = 6
BALL_SPEED_X = 5
BALL_SPEED_Y = 4
WIN_SCORE = 5
TICK_MS = 16


class PongGame:
    def __init__(self, root):
        self.root = root
        root.title("Pong")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                                bg="black", highlightthickness=0)
        self.canvas.pack()
        self.canvas.focus_set()
        root.bind("<KeyPress>", self._key_down)
        root.bind("<KeyRelease>", self._key_up)
        self.keys = set()
        self.left = self.canvas.create_rectangle(
            PADDLE_MARGIN, HEIGHT // 2 - PADDLE_H // 2,
            PADDLE_MARGIN + PADDLE_W, HEIGHT // 2 + PADDLE_H // 2, fill="white")
        self.right = self.canvas.create_rectangle(
            WIDTH - PADDLE_MARGIN - PADDLE_W, HEIGHT // 2 - PADDLE_H // 2,
            WIDTH - PADDLE_MARGIN, HEIGHT // 2 + PADDLE_H // 2, fill="white")
        self.ball = self.canvas.create_oval(0, 0, BALL_SIZE, BALL_SIZE, fill="white")
        self.canvas.create_line(WIDTH // 2, 0, WIDTH // 2, HEIGHT,
                                fill="white", dash=(4, 8))
        self.left_score_text = self.canvas.create_text(
            WIDTH // 4, 30, text="0", fill="white", font=("Arial", 32, "bold"))
        self.right_score_text = self.canvas.create_text(
            3 * WIDTH // 4, 30, text="0", fill="white", font=("Arial", 32, "bold"))
        self.message = None
        self.scores = [0, 0]
        self.winner = None
        self.ball_vx = 0
        self.ball_vy = 0
        self.reset_game()
        self.root.after(TICK_MS, self._tick)

    def _key_down(self, event):
        key = event.keysym.lower()
        if key == "r" and self.winner is not None:
            self.reset_game()
        self.keys.add(key)

    def _key_up(self, event):
        self.keys.discard(event.keysym.lower())

    def reset_game(self):
        self.scores = [0, 0]
        self.winner = None
        self.canvas.itemconfigure(self.left_score_text, text="0")
        self.canvas.itemconfigure(self.right_score_text, text="0")
        if self.message is not None:
            self.canvas.delete(self.message)
            self.message = None
        for paddle in (self.left, self.right):
            _, y1, _, y2 = self.canvas.coords(paddle)
            self.canvas.move(paddle, 0, HEIGHT // 2 - (y1 + y2) / 2)
        self.reset_ball(random.choice([-1, 1]))

    def reset_ball(self, direction):
        cx, cy = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
        self.canvas.coords(self.ball, cx, cy, cx + BALL_SIZE, cy + BALL_SIZE)
        self.ball_vx = BALL_SPEED_X * direction
        self.ball_vy = random.choice([-1, 1]) * BALL_SPEED_Y

    def _tick(self):
        if self.winner is None:
            self._move_paddles()
            self._move_ball()
        self.root.after(TICK_MS, self._tick)

    def _move_paddles(self):
        for paddle, up_key, down_key in ((self.left, "w", "s"),
                                         (self.right, "up", "down")):
            dy = (PADDLE_SPEED if down_key in self.keys else 0) - \
                 (PADDLE_SPEED if up_key in self.keys else 0)
            if dy:
                self.canvas.move(paddle, 0, dy)
                _, y1, _, y2 = self.canvas.coords(paddle)
                if y1 < 0:
                    self.canvas.move(paddle, 0, -y1)
                elif y2 > HEIGHT:
                    self.canvas.move(paddle, 0, HEIGHT - y2)

    def _move_ball(self):
        self.canvas.move(self.ball, self.ball_vx, self.ball_vy)
        x1, y1, x2, y2 = self.canvas.coords(self.ball)
        if y1 <= 0 and self.ball_vy < 0:
            self.ball_vy *= -1
            self.canvas.move(self.ball, 0, -y1)
        elif y2 >= HEIGHT and self.ball_vy > 0:
            self.ball_vy *= -1
            self.canvas.move(self.ball, 0, HEIGHT - y2)
        x1, y1, x2, y2 = self.canvas.coords(self.ball)
        for paddle, going_left in ((self.left, True), (self.right, False)):
            px1, py1, px2, py2 = self.canvas.coords(paddle)
            if x1 < px2 and x2 > px1 and y1 < py2 and y2 > py1:
                if going_left and self.ball_vx < 0:
                    self.ball_vx = abs(self.ball_vx)
                    self.canvas.move(self.ball, px2 - x1, 0)
                    self._deflect(py1, py2)
                elif not going_left and self.ball_vx > 0:
                    self.ball_vx = -abs(self.ball_vx)
                    self.canvas.move(self.ball, px1 - x2, 0)
                    self._deflect(py1, py2)
        x1, _, x2, _ = self.canvas.coords(self.ball)
        if x2 < 0:
            self._score(1, -1)
        elif x1 > WIDTH:
            self._score(0, 1)

    def _deflect(self, py1, py2):
        ball_y = sum(self.canvas.coords(self.ball)[1::2]) / 2
        offset = (ball_y - (py1 + py2) / 2) / (PADDLE_H / 2)
        self.ball_vy = int(BALL_SPEED_Y * offset) or random.choice([-1, 1]) * 2

    def _score(self, index, direction):
        self.scores[index] += 1
        text = self.left_score_text if index == 0 else self.right_score_text
        self.canvas.itemconfigure(text, text=str(self.scores[index]))
        if self.scores[index] >= WIN_SCORE:
            self.winner = index
            self.message = self.canvas.create_text(
                WIDTH // 2, HEIGHT // 2 - 20,
                text="Player %d wins! Press R to restart" % (index + 1),
                fill="white", font=("Arial", 24, "bold"))
        else:
            self.reset_ball(direction)


def main():
    root = tk.Tk()
    PongGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()