'''
bird.py
The Bird entity: gravity integration, flap impulse, motion-based
rotation, wing animation and self-contained sprite rendering (drawn
with pygame primitives, so no external image assets are required).
'''
import math
import pygame
import settings
class Bird:
    """Player-controlled bird that falls under gravity and flaps on input."""
    def __init__(self, x, y):
        """Place the bird at its spawn point with zero velocity."""
        self.start_x = float(x)
        self.start_y = float(y)
        self.x = float(x)
        self.y = float(y)
        self.velocity = 0.0
        self.rotation = 0.0
        self.wing_phase = 0.0
        self.alive = True
    ...