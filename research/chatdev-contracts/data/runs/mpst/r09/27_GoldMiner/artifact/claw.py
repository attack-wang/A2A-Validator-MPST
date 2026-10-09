'''
claw.py
The player-controlled claw that swings, shoots and reels in objects.
'''
import math
import pygame
import config
from objects import GameObject
class Claw:
    """Swinging claw on a rope. States: swinging -> extending -> retracting."""
    SWINGING = "swinging"
    EXTENDING = "extending"
    RETRACTING = "retracting"
    def __init__(self):
        self.pivot = (config.CLAW_PIVOT_X, config.CLAW_PIVOT_Y)
        self.angle = 0.0            # degrees, 0 = straight down
        self.swing_dir = 1
        self.swing_speed = config.CLAW_SWING_SPEED
        self.length = config.CLAW_MIN_LENGTH
        self.state = self.SWINGING
        self.attached = None        # GameObject being reeled in
        self.extend_speed = config.CLAW_EXTEND_SPEED
        self.retract_speed = config.CLAW_RETRACT_SPEED
    # ------------------------------------------------------------------ #
    @property
    def tip(self):
        """Current position of the claw tip."""
        rad = math.radians(self.angle)
        return (self.pivot[0] + math.sin(rad) * self.length,
                self.pivot[1] + math.cos(rad) * self.length)
    def is_busy(self):
        return self.state != self.SWINGING
    def launch(self):
        if self.state == self.SWINGING:
            self.state = self.EXTENDING
    def set_swing_speed(self, speed):
        self.swing_speed = speed
    # ------------------------------------------------------------------ #
    def update(self, objects, on_grab, on_deliver, on_tnt):
        """
        Advance the claw one frame.
        objects    : list of GameObjects in the field
        on_grab    : callback(object) when an object is grabbed
        on_deliver : callback(object) when an object is reeled to the top
        on_tnt     : callback(object) when TNT is touched (explosion)
        """
        if self.state == self.SWINGING:
            self.angle += self.swing_dir * self.swing_speed
            if self.angle >= config.CLAW_MAX_ANGLE:
                self.angle = config.CLAW_MAX_ANGLE
                self.swing_dir = -1
            elif self.angle <= -config.CLAW_MAX_ANGLE:
                self.angle = -config.CLAW_MAX_ANGLE
                self.swing_dir = 1
        elif self.state == self.EXTENDING:
            self.length += self.extend_speed
            tx, ty = self.tip
            # hit an object?
            for obj in objects:
                if obj.collected or obj.grabbed:
                    continue
                if obj.collides_with(tx, ty, config.CLAW_SIZE * 0.5):
                    if obj.kind == "tnt":
                        self.state = self.RETRACTING
                        self.attached = None
                        on_tnt(obj)
                        return
                    obj.grabbed = True
                    self.attached = obj
                    self.state = self.RETRACTING
                    on_grab(obj)
                    return
            # out of bounds?
            if (tx < 0 or tx > config.SCREEN_WIDTH or
                    ty > config.SCREEN_HEIGHT - 10):
                self.state = self.RETRACTING
        elif self.state == self.RETRACTING:
            weight = self.attached.weight if self.attached else 1.0
            speed = self.retract_speed / max(weight, 0.5)
            self.length -= speed
            if self.attached:
                tx, ty = self.tip
                self.attached.x = tx
                self.attached.y = ty + 6
            if self.length <= config.CLAW_MIN_LENGTH:
                self.length = config.CLAW_MIN_LENGTH
                delivered = self.attached
                self.attached = None
                self.state = self.SWINGING
                if delivered:
                    delivered.grabbed = False
                    delivered.collected = True
                    on_deliver(delivered)
    # ------------------------------------------------------------------ #
    def draw(self, surface):
        pygame.draw.line(surface, config.COLOR_ROPE, self.pivot, self.tip, 3)
        # draw the claw as a small "V" pincer oriented along the rope
        ...