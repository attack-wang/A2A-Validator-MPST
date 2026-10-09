'''
alien.py
A single invader. Aliens know their row (which sets their colour and
point value), move with the fleet and can be drawn with a simple
two-frame animation using tkinter canvas shapes.
'''
from settings import Settings
class Alien:
    """One invader inside the fleet grid."""
    def __init__(self, game, row, col, x, y):
        self.game = game
        self.row = row
        self.col = col
        points_table = Settings.ALIEN_POINTS
        self.points = points_table[min(row, len(points_table) - 1)]
        self.color = Settings.ALIEN_COLORS[min(row, len(Settings.ALIEN_COLORS) - 1)]
        self.width = Settings.ALIEN_WIDTH
        self.height = Settings.ALIEN_HEIGHT
        self.x = float(x)
        self.y = float(y)
        self.alive = True
        self.animation_frame = 0
    @property
    def rect(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)
    def update_position(self, dx, dy):
        if not self.alive:
            return
        self.x += dx
        self.y += dy
    def set_animation_frame(self, frame):
        self.animation_frame = frame
    def draw(self, canvas):
        if not self.alive:
            return
        x, y = int(self.x), int(self.y)
        w, h = self.width, self.height
        c = self.color
        dark = "#0a0a14"
        # Main body
        canvas.create_rectangle(x + 4, y + 4, x + w - 4, y + h - 8, fill=c, outline="")
        # Eyes
        canvas.create_rectangle(x + 8, y + 8, x + 13, y + 13, fill=dark, outline="")
        canvas.create_rectangle(x + w - 13, y + 8, x + w - 8, y + 13, fill=dark, outline="")
        # Legs - two frames for a walking animation
        if self.animation_frame == 0:
            canvas.create_rectangle(x + 6, y + h - 8, x + 12, y + h, fill=c, outline="")
            canvas.create_rectangle(x + w - 12, y + h - 8, x + w - 6, y + h, fill=c, outline="")
            canvas.create_rectangle(x + w // 2 - 3, y + h - 6, x + w // 2 + 3, y + h, fill=c, outline="")
        else:
            canvas.create_rectangle(x + 10, y + h - 8, x + 16, y + h, fill=c, outline="")
            canvas.create_rectangle(x + w - 16, y + h - 8, x + w - 10, y + h, fill=c, outline="")
        # Antennae
        canvas.create_rectangle(x + 8, y, x + 12, y + 5, fill=c, outline="")
        canvas.create_rectangle(x + w - 12, y, x + w - 8, y + 5, fill=c, outline="")