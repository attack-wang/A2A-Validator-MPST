import tkinter as tk

from bird import Bird
from pipe import Pipe

WIDTH, HEIGHT = 480, 640
GROUND_H = 80
FPS_MS = 16
PIPE_SPACING = 230
SKY = "#71c5cf"
GROUND_COL = "#deb887"
GROUND_EDGE = "#a07850"


class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Flappy Bird")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT,
                                bg=SKY, highlightthickness=0)
        self.canvas.pack()
        for key in ("<space>", "<Up>"):
            self.root.bind(key, lambda e: self.flap())
        self.reset()

    def reset(self):
        self.bird = Bird(WIDTH // 4, (HEIGHT - GROUND_H) // 2)
        self.pipes = []
        self.score = 0
        self.speed = 3.0
        self.base_gap = 175
        self.started = False
        self.game_over = False

    def apply_difficulty(self):
        self.speed = min(3.0 + self.score * 0.08, 7.5)
        self.base_gap = max(120, 175 - self.score * 2)

    def flap(self):
        if self.game_over:
            self.reset()
        elif not self.started:
            self.started = True
            self.bird.flap()
        else:
            self.bird.flap()

    def update(self):
        if self.game_over or not self.started:
            return
        self.apply_difficulty()
        self.bird.update()
        if not self.pipes or self.pipes[-1].x <= WIDTH - PIPE_SPACING:
            self.pipes.append(Pipe(WIDTH, HEIGHT - GROUND_H, self.base_gap))
        for pipe in self.pipes:
            pipe.update(self.speed)
            if not pipe.scored and pipe.x + pipe.width < self.bird.x:
                pipe.scored = True
                self.score += 1
        self.pipes = [p for p in self.pipes if not p.offscreen()]
        if self.bird.y + self.bird.radius >= HEIGHT - GROUND_H:
            self.bird.y = HEIGHT - GROUND_H - self.bird.radius
            self.game_over = True
        if any(p.collides(self.bird.rect) for p in self.pipes):
            self.game_over = True

    def draw(self):
        c = self.canvas
        c.delete("all")
        for pipe in self.pipes:
            pipe.draw(c)
        c.create_rectangle(0, HEIGHT - GROUND_H, WIDTH, HEIGHT,
                           fill=GROUND_COL, width=0)
        c.create_rectangle(0, HEIGHT - GROUND_H, WIDTH, HEIGHT - GROUND_H + 10,
                           fill=GROUND_EDGE, width=0)
        self.bird.draw(c)
        c.create_text(WIDTH // 2, 30, text=str(self.score),
                      font=("Arial", 28, "bold"), fill="white")
        if not self.started:
            c.create_text(WIDTH // 2, HEIGHT // 2, text="Press SPACE to flap",
                          font=("Arial", 16), fill="white")
        elif self.game_over:
            c.create_text(WIDTH // 2, HEIGHT // 2 - 30, text="Game Over!",
                          font=("Arial", 28, "bold"), fill="#c81e1e")
            c.create_text(WIDTH // 2, HEIGHT // 2 + 10,
                          text="Score: %d - Press SPACE to restart" % self.score,
                          font=("Arial", 14), fill="white")

    def loop(self):
        self.update()
        self.draw()
        self.root.after(FPS_MS, self.loop)

    def run(self):
        self.loop()
        self.root.mainloop()