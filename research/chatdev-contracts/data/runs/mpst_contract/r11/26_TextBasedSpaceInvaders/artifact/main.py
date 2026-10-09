import random
import tkinter as tk

WIDTH, HEIGHT = 640, 720
TICK_MS = 16

PLAYER_SPEED = 5
BULLET_SPEED = 8
ALIEN_BULLET_SPEED = 4
ALIEN_ROWS = 4
ALIEN_COLS = 8
ALIEN_DESCEND = 20
START_LIVES = 3

BG = "#0a0a14"
FG = "#f0f0f0"
GREEN = "#50dc64"
RED = "#e65050"
CYAN = "#50c8e6"
YELLOW = "#f0dc50"


class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Space Invaders")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT,
                                bg=BG, highlightthickness=0)
        self.canvas.pack()
        self.keys = set()
        self.root.bind("<KeyPress>", self._key_down)
        self.root.bind("<KeyRelease>", self._key_up)
        self.reset()
        self.root.after(TICK_MS, self.tick)
        self.root.mainloop()

    def _key_down(self, e):
        k = e.keysym.lower()
        self.keys.add(k)
        if self.state != "play":
            if k == "r":
                self.reset()
            elif k == "q":
                self.root.destroy()

    def _key_up(self, e):
        self.keys.discard(e.keysym.lower())

    def reset(self):
        self.player_x = WIDTH // 2 - 24
        self.player_y = HEIGHT - 60
        self.cooldown = 0
        self.bullets = []
        self.alien_bullets = []
        self.aliens = [[60 + c * 60, 60 + r * 50, (ALIEN_ROWS - r) * 10]
                       for r in range(ALIEN_ROWS) for c in range(ALIEN_COLS)]
        self.alien_dir = 1
        self.alien_timer = 0.0
        self.score = 0
        self.lives = START_LIVES
        self.state = "play"

    def alien_speed(self):
        return 0.5 + (ALIEN_ROWS * ALIEN_COLS - len(self.aliens)) * 0.03

    def tick(self):
        if self.state == "play":
            self.update()
        self.draw()
        self.root.after(TICK_MS, self.tick)

    def update(self):
        if "left" in self.keys or "a" in self.keys:
            self.player_x -= PLAYER_SPEED
        if "right" in self.keys or "d" in self.keys:
            self.player_x += PLAYER_SPEED
        self.player_x = max(0, min(WIDTH - 48, self.player_x))
        if self.cooldown > 0:
            self.cooldown -= 1
        if "space" in self.keys and self.cooldown <= 0:
            self.bullets.append([self.player_x + 22, self.player_y - 12])
            self.cooldown = 18

        for b in self.bullets[:]:
            b[1] -= BULLET_SPEED
            if b[1] < -12:
                self.bullets.remove(b)
                continue
            for a in self.aliens[:]:
                if (b[0] < a[0] + 36 and b[0] + 4 > a[0] and
                        b[1] < a[1] + 24 and b[1] + 12 > a[1]):
                    self.aliens.remove(a)
                    self.score += a[2]
                    if b in self.bullets:
                        self.bullets.remove(b)
                    break

        if self.aliens:
            self.alien_timer += self.alien_speed()
            step = int(self.alien_timer)
            if step >= 1:
                self.alien_timer -= step
                dx = self.alien_dir * step * 6
                min_x = min(a[0] for a in self.aliens)
                max_x = max(a[0] + 36 for a in self.aliens)
                descend = False
                if max_x + dx >= WIDTH - 10 or min_x + dx <= 10:
                    self.alien_dir *= -1
                    dx = self.alien_dir * step * 6
                    descend = True
                for a in self.aliens:
                    a[0] += dx
                    if descend:
                        a[1] += ALIEN_DESCEND
                if max(a[1] + 24 for a in self.aliens) >= self.player_y:
                    self.state = "lose"
                    return

            if random.random() < 0.02:
                s = random.choice(self.aliens)
                self.alien_bullets.append([s[0] + 16, s[1] + 24])

        for b in self.alien_bullets[:]:
            b[1] += ALIEN_BULLET_SPEED
            if b[1] > HEIGHT:
                self.alien_bullets.remove(b)
                continue
            if (b[0] < self.player_x + 48 and b[0] + 4 > self.player_x and
                    b[1] < self.player_y + 20 and b[1] + 10 > self.player_y):
                self.alien_bullets.remove(b)
                self.lives -= 1
                if self.lives <= 0:
                    self.state = "lose"
                    return

        if not self.aliens:
            self.state = "win"

    def draw(self):
        c = self.canvas
        c.delete("all")
        px, py = self.player_x, self.player_y
        c.create_polygon(px + 24, py, px + 48, py + 20,
                         px + 24, py + 14, px, py + 20, fill=CYAN)
        for b in self.bullets:
            c.create_rectangle(b[0], b[1], b[0] + 4, b[1] + 12,
                               fill=YELLOW, width=0)
        for b in self.alien_bullets:
            c.create_rectangle(b[0], b[1], b[0] + 4, b[1] + 10,
                               fill=RED, width=0)
        for a in self.aliens:
            x, y = a[0], a[1]
            c.create_rectangle(x + 4, y, x + 32, y + 24, fill=GREEN, width=0)
            c.create_rectangle(x, y + 6, x + 36, y + 14, fill=GREEN, width=0)
            c.create_rectangle(x + 8, y + 8, x + 14, y + 14, fill=BG, width=0)
            c.create_rectangle(x + 22, y + 8, x + 28, y + 14, fill=BG, width=0)
        c.create_text(10, 10, anchor="nw",
                      text=f"Score: {self.score}   Lives: {self.lives}",
                      fill=FG, font=("Helvetica", 16))
        if self.state != "play":
            msg = "YOU WIN!" if self.state == "win" else "GAME OVER"
            color = YELLOW if self.state == "win" else RED
            c.create_text(WIDTH // 2, HEIGHT // 2 - 20, text=msg,
                          fill=color, font=("Helvetica", 36, "bold"))
            c.create_text(WIDTH // 2, HEIGHT // 2 + 30,
                          text="Press R to restart, Q to quit",
                          fill=FG, font=("Helvetica", 14))


if __name__ == "__main__":
    Game()