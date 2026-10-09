"""Claw: swinging, extending, grabbing and reeling logic."""
import math
import pygame
from settings import *
CLAW_SWING = "swing"
CLAW_EXTEND = "extend"
CLAW_RETRACT = "retract"
def segment_circle_intersect(p1, p2, c, r):
    """True if the segment p1-p2 comes within r of point c."""
    (x1, y1), (x2, y2) = p1, p2
    cx, cy = c
    dx, dy = x2 - x1, y2 - y1
    len2 = dx * dx + dy * dy
    if len2 == 0:
        return math.hypot(cx - x1, cy - y1) <= r
    t = ((cx - x1) * dx + (cy - y1) * dy) / len2
    t = max(0, min(1, t))
    closest = (x1 + t * dx, y1 + t * dy)
    return math.hypot(cx - closest[0], cy - closest[1]) <= r
class Claw:
    def __init__(self):
        self.pivot = PIVOT
        self.angle = 0.0
        self.direction = 1
        self.state = CLAW_SWING
        self.length = ROPE_MIN
        self.grabbed = None
        self.fuse = 0.0
        self.swing_speed = BASE_SWING
        self.swing_min = -SWING_LIMIT
        self.swing_max = SWING_LIMIT
    @property
    def tip(self):
        px, py = self.pivot
        return (px + math.sin(self.angle) * self.length,
                py + math.cos(self.angle) * self.length)
    def set_level_speed(self, speed):
        self.swing_speed = speed
    def launch(self):
        if self.state == CLAW_SWING:
            self.state = CLAW_EXTEND
    def update(self, dt, objects, on_deposit, on_explode):
        ...