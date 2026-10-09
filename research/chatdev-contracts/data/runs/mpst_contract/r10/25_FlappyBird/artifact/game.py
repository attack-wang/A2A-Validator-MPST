import tkinter as tk
from settings import *
from entities import Bird, Pipe


class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Flappy Bird")
        self.root.resizable(False, False)
        self.cv = tk.Canvas(self.root, width=WIDTH, height=HEIGHT,
                            bg=SKY, highlightthickness=0)
        self.cv.pack()
        self.best = 0
        self.root.bind("<KeyPress>", self.on_key)
        self.root.bind("<Button-1>", self.on_click)
        self.reset()
        self.root.after(FPS_MS, self.loop)

    def reset(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.spawn = 0
        self.state = "menu"
        self.ground_x = 0.0

    @staticmethod
    def is_flap(keysym):
        return keysym in ("space", "Up", "w")

    def restart(self):
        best = self.best
        self.reset()
        self.best = best

    def on_key(self, e):
        if e.keysym == "Escape":
            self.root.destroy()
            return
        if self.state == "menu" and self.is_flap(e.keysym):
            self.state = "play"
            self.bird.flap()
        elif self.state == "play" and self.is_flap(e.keysym):
            self.bird.flap()
        elif self.state == "over" and (self.is_flap(e.keysym) or e.keysym == "r"):
            self.restart()

    def on_click(self, e):
        if self.state == "menu":
            self.state = "play"
            self.bird.flap()
        elif self.state == "play":
            self.bird.flap()
        elif self.state == "over":
            self.restart()

    def current_speed(self):
        return min(BASE_SPEED + self.score * SPEED_GAIN, MAX_SPEED)

    def update(self):
        if self.state != "play":
            return
        self.bird.update()
        self.ground_x = (self.ground_x + self.current_speed()) % 24
        self.spawn += 1
        if self.spawn >= SPAWN_FRAMES or not self.pipes:
            self.spawn = 0
            self.pipes.append(Pipe(WIDTH + 10, self.score))
        for p in self.pipes:
            p.update()
            if not p.passed and p.x + PIPE_W < self.bird.x:
                p.passed = True
                self.score += 1
            if p.collides(self.bird):
                self.game_over()
                return
        self.pipes = [p for p in self.pipes if not p.offscreen()]
        if not self.bird.alive:
            self.game_over()

    def game_over(self):
        self.state = "over"
        self.best = max(self.best, self.score)

    def draw_ground(self):
        gh = HEIGHT - GROUND_H
        self.cv.create_rectangle(0, gh, WIDTH, HEIGHT, fill=GROUND, outline="")
        self.cv.create_rectangle(0, gh, WIDTH, gh + 6, fill=PIPE_DARK, outline="")
        x = -int(self.ground_x)
        while x < WIDTH:
            self.cv.create_rectangle(x, gh + 12, x + 12, gh + 20,
                                     fill=GROUND_STRIPE, outline="")
            x += 24

    def center_text(self, text, y, font, fill=WHITE):
        self.cv.create_text(WIDTH // 2 + 2, y + 2, text=text, font=font, fill=BLACK)
        self.cv.create_text(WIDTH // 2, y, text=text, font=font, fill=fill)

    def draw(self):
        self.cv.delete("all")
        for p in self.pipes:
            p.draw(self.cv)
        self.draw_ground()
        self.bird.draw(self.cv)
        self.cv.create_text(WIDTH // 2 + 2, 52, text=str(self.score),
                            font=FONT, fill=BLACK)
        self.cv.create_text(WIDTH // 2, 50, text=str(self.score),
                            font=FONT, fill=WHITE)
        if self.state == "menu":
            self.center_text("Press SPACE / UP to flap", HEIGHT // 2 - 40, SMALL_FONT)
        elif self.state == "over":
            self.center_text("Game Over", HEIGHT // 2 - 60, FONT, ORANGE)
            self.center_text("Score: %d  Best: %d" % (self.score, self.best),
                             HEIGHT // 2 - 10, SMALL_FONT)
            self.center_text("SPACE to restart", HEIGHT // 2 + 30, SMALL_FONT)

    def loop(self):
        self.update()
        self.draw()
        self.root.after(FPS_MS, self.loop)

    def run(self):
        self.root.mainloop()