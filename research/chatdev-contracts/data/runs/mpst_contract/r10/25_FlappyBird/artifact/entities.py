import random
from settings import *


class Bird:
    def __init__(self):
        self.x = BIRD_X
        self.y = HEIGHT // 3
        self.vel = 0.0
        self.alive = True
        self.wing = 0

    def flap(self):
        self.vel = FLAP_STRENGTH
        self.wing = 10

    def update(self):
        self.vel = min(self.vel + GRAVITY, MAX_FALL_SPEED)
        self.y += self.vel
        if self.wing > 0:
            self.wing -= 1
        floor = HEIGHT - GROUND_H - BIRD_R
        if self.y >= floor:
            self.y = floor
            self.alive = False
        if self.y < BIRD_R:
            self.y = BIRD_R
            self.vel = 0

    def box(self):
        pad = 3
        s = (BIRD_R - pad) * 2
        x1 = self.x - BIRD_R + pad
        y1 = self.y - BIRD_R + pad
        return (x1, y1, x1 + s, y1 + s)

    def collides(self, rects):
        b = self.box()
        for (x1, y1, x2, y2) in rects:
            if not (b[2] < x1 or b[0] > x2 or b[3] < y1 or b[1] > y2):
                return True
        return False

    def draw(self, cv):
        cx, cy = int(self.x), int(self.y)
        cv.create_oval(cx - BIRD_R, cy - BIRD_R, cx + BIRD_R, cy + BIRD_R,
                       fill=YELLOW, outline=BLACK, width=2)
        wy = cy + (4 if self.wing > 0 else 0)
        cv.create_oval(cx - 10, wy - 2, cx + 6, wy + 6, fill=ORANGE, outline="")
        cv.create_oval(cx + 1, cy - 9, cx + 9, cy - 1, fill=WHITE, outline="")
        cv.create_oval(cx + 4, cy - 7, cx + 8, cy - 3, fill=BLACK, outline="")
        cv.create_polygon(cx + BIRD_R - 2, cy - 2, cx + BIRD_R + 8, cy,
                          cx + BIRD_R - 2, cy + 5, fill=ORANGE, outline="")


class Pipe:
    def __init__(self, x, score):
        self.speed = min(BASE_SPEED + score * SPEED_GAIN, MAX_SPEED)
        gap = BASE_GAP - score * GAP_SHRINK + random.randint(-GAP_VARIANCE, GAP_VARIANCE)
        self.gap = max(MIN_GAP, gap)
        self.x = float(x)
        margin = 50
        lo = margin
        hi = HEIGHT - GROUND_H - margin - self.gap
        self.top = random.randint(int(lo), int(max(lo, hi)))
        self.bottom = self.top + self.gap
        self.passed = False

    def update(self):
        self.x -= self.speed

    def offscreen(self):
        return self.x + PIPE_W < -10

    def rects(self):
        return ((self.x, 0, self.x + PIPE_W, self.top),
                (self.x, self.bottom, self.x + PIPE_W, HEIGHT - GROUND_H))

    def collides(self, bird):
        return bird.collides(self.rects())

    def draw(self, cv):
        for (x1, y1, x2, y2) in self.rects():
            cv.create_rectangle(x1, y1, x2, y2, fill=PIPE_GREEN,
                                outline=PIPE_DARK, width=3)
            cap_y = y2 - 24 if y1 == 0 else y1
            cv.create_rectangle(x1 - 4, cap_y, x2 + 4, cap_y + 24,
                                fill=PIPE_GREEN, outline=PIPE_DARK, width=3)