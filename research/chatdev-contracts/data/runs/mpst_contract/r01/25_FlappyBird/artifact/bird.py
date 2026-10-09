GRAVITY = 0.45
FLAP_STRENGTH = -8.5
MAX_FALL = 11.0
BODY = "#ffcc00"
WING = "#e6a000"
BEAK = "#ff7800"


class Bird:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vel = 0.0
        self.radius = 13
        self.update_rect()

    def flap(self):
        self.vel = FLAP_STRENGTH

    def update_rect(self):
        r = self.radius
        self.rect = (int(self.x) - r, int(self.y) - r,
                     int(self.x) + r, int(self.y) + r)

    def update(self):
        self.vel = min(self.vel + GRAVITY, MAX_FALL)
        self.y += self.vel
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vel = 0
        self.update_rect()

    def draw(self, c):
        x, y, r = int(self.x), int(self.y), self.radius
        c.create_oval(x - r, y - r, x + r, y + r, fill=BODY, outline="#cc9900")
        c.create_oval(x - 1, y - 8, x + 9, y, fill="white", width=0)
        c.create_oval(x + 3, y - 6, x + 7, y - 2, fill="black", width=0)
        c.create_polygon(x + r - 2, y, x + r + 6, y + 2, x + r - 2, y + 5,
                         fill=BEAK, width=0)
        c.create_oval(x - 8, y, x + 4, y + 8, fill=WING, width=0)