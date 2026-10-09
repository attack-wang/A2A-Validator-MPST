import math
import random
import tkinter as tk

WIDTH, HEIGHT = 800, 600
PADDLE_W, PADDLE_H = 12, 90
PADDLE_SPEED = 6
BALL_SIZE = 14
BALL_SPEED = 5.0
MAX_VY = 8.0
WINNING_SCORE = 5
FRAME_MS = 16


class PongGame:
    def __init__(self, root):
        self.root = root
        root.title("Pong - P1: W/S   P2: Up/Down   R: restart   ESC: quit")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                                bg="black", highlightthickness=0)
        self.canvas.pack()
        self.canvas.focus_set()
        self.keys = set()

        self.left_score = 0
        self.right_score = 0
        self.winner = None

        self.lx = 30.0
        self.rx = WIDTH - 30.0 - PADDLE_W
        self.ly = self.ry = (HEIGHT - PADDLE_H) / 2.0

        self.canvas.create_line(WIDTH / 2, 0, WIDTH / 2, HEIGHT,
                                fill="white", dash=(4, 8))
        self.left_item = self.canvas.create_rectangle(
            self.lx, self.ly, self.lx + PADDLE_W, self.ly + PADDLE_H, fill="white")
        self.right_item = self.canvas.create_rectangle(
            self.rx, self.ry, self.rx + PADDLE_W, self.ry + PADDLE_H, fill="white")
        self.ball_item = self.canvas.create_oval(
            0, 0, BALL_SIZE, BALL_SIZE, fill="white")
        self.l_score_item = self.canvas.create_text(
            WIDTH / 2 - 60, 40, text="0", fill="white", font=("Consolas", 40, "bold"))
        self.r_score_item = self.canvas.create_text(
            WIDTH / 2 + 60, 40, text="0", fill="white", font=("Consolas", 40, "bold"))
        self.msg_item = self.canvas.create_text(
            WIDTH / 2, HEIGHT / 2, text="", fill="white", font=("Consolas", 20))

        root.bind("<KeyPress>", self.key_down)
        root.bind("<KeyRelease>", self.key_up)

        self.reset_ball()
        self.loop()

    def reset_ball(self):
        self.bx = WIDTH / 2.0
        self.by = HEIGHT / 2.0
        angle = random.uniform(-math.pi / 6, math.pi / 6)
        self.bvx = random.choice((-1.0, 1.0)) * BALL_SPEED * math.cos(angle)
        self.bvy = BALL_SPEED * math.sin(angle)

    def key_down(self, event):
        sym = event.keysym.lower()
        if sym == "escape":
            self.root.destroy()
            return
        self.keys.add(sym)
        if sym == "r" and self.winner:
            self.left_score = 0
            self.right_score = 0
            self.winner = None
            self.ly = self.ry = (HEIGHT - PADDLE_H) / 2.0
            self.reset_ball()

    def key_up(self, event):
        self.keys.discard(event.keysym.lower())

    def move_paddles(self):
        if "w" in self.keys:
            self.ly -= PADDLE_SPEED
        if "s" in self.keys:
            self.ly += PADDLE_SPEED
        if "up" in self.keys:
            self.ry -= PADDLE_SPEED
        if "down" in self.keys:
            self.ry += PADDLE_SPEED
        self.ly = max(0.0, min(HEIGHT - PADDLE_H, self.ly))
        self.ry = max(0.0, min(HEIGHT - PADDLE_H, self.ry))

    def hits(self, px, py):
        return (self.bx + BALL_SIZE / 2.0 >= px
                and self.bx - BALL_SIZE / 2.0 <= px + PADDLE_W
                and self.by + BALL_SIZE / 2.0 >= py
                and self.by - BALL_SIZE / 2.0 <= py + PADDLE_H)

    def spin(self, py):
        return (self.by - (py + PADDLE_H / 2.0)) / (PADDLE_H / 2.0) * 2.5

    def update(self):
        if self.winner:
            return
        self.move_paddles()

        self.bx += self.bvx
        self.by += self.bvy
        if self.by - BALL_SIZE / 2.0 <= 0:
            self.by = BALL_SIZE / 2.0
            self.bvy = abs(self.bvy)
        elif self.by + BALL_SIZE / 2.0 >= HEIGHT:
            self.by = HEIGHT - BALL_SIZE / 2.0
            self.bvy = -abs(self.bvy)

        if self.bvx < 0 and self.hits(self.lx, self.ly):
            self.bx = self.lx + PADDLE_W + BALL_SIZE / 2.0
            self.bvx = abs(self.bvx)
            self.bvy += self.spin(self.ly)
        elif self.bvx > 0 and self.hits(self.rx, self.ry):
            self.bx = self.rx - BALL_SIZE / 2.0
            self.bvx = -abs(self.bvx)
            self.bvy += self.spin(self.ry)
        self.bvy = max(-MAX_VY, min(MAX_VY, self.bvy))

        if self.bx + BALL_SIZE / 2.0 <= 0:
            self.right_score += 1
            self.check_winner()
            self.reset_ball()
        elif self.bx - BALL_SIZE / 2.0 >= WIDTH:
            self.left_score += 1
            self.check_winner()
            self.reset_ball()

    def check_winner(self):
        if self.left_score >= WINNING_SCORE:
            self.winner = "Player 1"
        elif self.right_score >= WINNING_SCORE:
            self.winner = "Player 2"

    def draw(self):
        self.canvas.coords(self.left_item, self.lx, self.ly,
                           self.lx + PADDLE_W, self.ly + PADDLE_H)
        self.canvas.coords(self.right_item, self.rx, self.ry,
                           self.rx + PADDLE_W, self.ry + PADDLE_H)
        self.canvas.coords(self.ball_item, self.bx - BALL_SIZE / 2.0,
                           self.by - BALL_SIZE / 2.0,
                           self.bx + BALL_SIZE / 2.0,
                           self.by + BALL_SIZE / 2.0)
        self.canvas.itemconfigure(self.l_score_item, text=str(self.left_score))
        self.canvas.itemconfigure(self.r_score_item, text=str(self.right_score))
        self.canvas.itemconfigure(
            self.msg_item,
            text=f"{self.winner} wins!  R = restart, ESC = quit" if self.winner else "")

    def loop(self):
        try:
            self.update()
            self.draw()
            self.root.after(FRAME_MS, self.loop)
        except tk.TclError:
            return


def main():
    root = tk.Tk()
    PongGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()