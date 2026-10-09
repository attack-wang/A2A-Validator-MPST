import random

PIPE_WIDTH = 60
MARGIN = 60
MIN_GAP = 110
PIPE_COL = "#3ca03c"
PIPE_EDGE = "#1e641e"
PIPE_LIP = "#50c850"


class Pipe:
    def __init__(self, x, play_height, base_gap):
        self.x = float(x)
        self.play_height = play_height
        self.width = PIPE_WIDTH
        self.gap = max(MIN_GAP, min(int(random.gauss(base_gap, 18)), base_gap + 40))
        top_limit = play_height - MARGIN - self.gap
        self.gap_y = random.randint(MARGIN, max(MARGIN, top_limit))
        self.scored = False

    def update(self, speed):
        self.x -= speed

    def offscreen(self):
        return self.x + self.width < 0

    def collides(self, rect):
        bx1, by1, bx2, by2 = rect
        for rx1, ry1, rx2, ry2 in (
            (self.x, 0, self.x + self.width, self.gap_y),
            (self.x, self.gap_y + self.gap, self.x + self.width, self.play_height),
        ):
            if bx1 < rx2 and bx2 > rx1 and by1 < ry2 and by2 > ry1:
                return True
        return False

    def draw(self, c):
        x, w = int(self.x), self.width
        c.create_rectangle(x, 0, x + w, self.gap_y,
                           fill=PIPE_COL, outline=PIPE_EDGE, width=3)
        c.create_rectangle(x, self.gap_y + self.gap, x + w, self.play_height,
                           fill=PIPE_COL, outline=PIPE_EDGE, width=3)
        c.create_rectangle(x - 4, self.gap_y - 24, x + w + 4, self.gap_y,
                           fill=PIPE_LIP, outline=PIPE_EDGE)
        c.create_rectangle(x - 4, self.gap_y + self.gap, x + w + 4,
                           self.gap_y + self.gap + 24,
                           fill=PIPE_LIP, outline=PIPE_EDGE)