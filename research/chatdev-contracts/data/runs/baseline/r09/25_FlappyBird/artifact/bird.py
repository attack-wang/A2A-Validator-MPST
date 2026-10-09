'''
bird.py
Defines the Bird: physics integration, flap impulse, wing animation
and canvas rendering for the tkinter edition.
'''
import math
import settings
from utils import Rect
class Bird:
    """The player-controlled bird with gravity, flapping and rotation."""
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.velocity = 0.0
        self.rotation = 0.0
        self.wing_frame = 0
        self.wing_timer = 0.0
        self.alive = True
    @property
    def rect(self):
        """Collision box: slightly forgiving around the visual body."""
        r = settings.BIRD_RADIUS
        return Rect(int(self.x - r * 0.9), int(self.y - r * 0.8),
                    int(r * 2.3), int(r * 1.6))
    def flap(self):
        """Apply the upward flap impulse and kick the wing animation."""
        self.velocity = settings.FLAP_VELOCITY
        self.wing_frame = 1
        self.wing_timer = 0.0
    def update(self, dt):
        """Integrate gravity, clamp fall speed and animate wing/rotation."""
        self.velocity = min(self.velocity + settings.GRAVITY * dt,
                            settings.MAX_FALL_SPEED)
        self.y += self.velocity * dt
        # Rotation follows the vertical velocity (nose up on flap, dive down).
        target = max(-25.0, min(90.0, self.velocity / settings.MAX_FALL_SPEED * 90.0))
        blend = min(1.0, dt * 10.0)
        self.rotation += (target - self.rotation) * blend
        # Wing flapping animation (3 frames).
        self.wing_timer += dt
        if self.wing_timer > 0.12:
            self.wing_timer = 0.0
            self.wing_frame = (self.wing_frame + 1) % 3
    def draw(self, canvas, tag="frame"):
        """Draw the rotated bird as composed canvas shapes."""
        r = settings.BIRD_RADIUS
        rot = math.radians(-self.rotation)
        cos_r, sin_r = math.cos(rot), math.sin(rot)
        def transform(px, py):
            """Rotate a local point around the bird centre."""
            return (self.x + px * cos_r - py * sin_r,
                    self.y + px * sin_r + py * cos_r)
        def ellipse_points(cx, cy, rx, ry, steps=14):
            pts = []
            for i in range(steps):
                a = 2.0 * math.pi * i / steps
                px, py = transform(cx + rx * math.cos(a), cy + ry * math.sin(a))
                pts.extend((px, py))
            return pts
        # Body (rotated ellipse drawn as a smooth polygon).
        canvas.create_polygon(ellipse_points(0, 0, r, r * 0.85),
                              fill=settings.BIRD_COLOR,
                              outline=settings.PIPE_EDGE, smooth=True, tag=tag)
        # Belly highlight.
        canvas.create_polygon(ellipse_points(-r * 0.1, r * 0.35, r * 0.6, r * 0.45),
                              fill=settings.BIRD_BELLY, outline="", smooth=True, tag=tag)
        # Eye.
        ex, ey = transform(r * 0.45, -r * 0.35)
        er = r * 0.38
        canvas.create_oval(ex - er, ey - er, ex + er, ey + er,
                           fill="white", outline="", tag=tag)
        canvas.create_oval(ex + er * 0.2, ey - er * 0.2,
                           ex + er * 1.0, ey + er * 0.6,
                           fill="#1e1e1e", outline="", tag=tag)
        # Beak.
        p1 = transform(r * 0.8, -r * 0.05)
        p2 = transform(r * 1.5, r * 0.15)
        p3 = transform(r * 0.8, r * 0.35)
        canvas.create_polygon(p1, p2, p3, fill=settings.BIRD_BEAK,
                              outline="", tag=tag)
        # Wing (3 animation frames).
        wing_y = r * 0.1
        if self.wing_frame == 0:
            wy = wing_y
        elif self.wing_frame == 1:
            wy = wing_y - r * 0.35
        else:
            wy = wing_y + r * 0.3
        canvas.create_polygon(ellipse_points(-r * 0.35, wy, r * 0.55, r * 0.28),
                              fill=settings.BIRD_WING, outline="", smooth=True, tag=tag)