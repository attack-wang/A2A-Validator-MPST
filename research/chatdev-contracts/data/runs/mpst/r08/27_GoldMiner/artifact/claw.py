'''
The miner's claw: swings, extends, grabs, and reels in objects.
'''
import math
import pygame
from settings import (PIVOT, CLAW_MIN_LENGTH, CLAW_MAX_ANGLE, CLAW_TIP_RADIUS,
                      CLAW_MAX_LENGTH, CLAW_RETRACT_EMPTY_SPEED,
                      CLAW_RETRACT_BASE_SPEED, GRAY_DARK, BLACK)
SWING, EXTEND, RETRACT = 'swing', 'extend', 'retract'
class Claw:
    """Swings under the pulley, extends on demand, grabs one object and
    reels it back. update() returns one event string per frame or None:
    'grab', 'deliver', 'miss' or 'tnt'.
    """
    def __init__(self):
        self.reset()
    def reset(self):
        self.angle = 0.0
        self.direction = 1
        self.length = CLAW_MIN_LENGTH
        self.state = SWING
        self.attached = None
        self.swing_speed = 70.0
        self.extend_speed = 420.0
    def launch(self):
        """Start extending if the claw is currently swinging."""
        if self.state == SWING:
            self.state = EXTEND
    def tip(self):
        """Current position of the claw tip as an (x, y) tuple."""
        rad = math.radians(self.angle)
        return (PIVOT[0] + math.sin(rad) * self.length,
                PIVOT[1] + math.cos(rad) * self.length)
    def update(self, dt, objects):
        """Advance claw state. Returns a string event or None:
        'grab', 'deliver', 'miss', 'tnt'."""
        event = None
        if self.state == SWING:
            self.angle += self.direction * self.swing_speed * dt
            if self.angle >= CLAW_MAX_ANGLE:
                self.angle = CLAW_MAX_ANGLE
                self.direction = -1
            elif self.angle <= -CLAW_MAX_ANGLE:
                self.angle = -CLAW_MAX_ANGLE
                self.direction = 1
        elif self.state == EXTEND:
            self.length += self.extend_speed * dt
            tip_x, tip_y = self.tip()
            for obj in objects:
                if obj.attached:
                    continue
                dist = math.hypot(tip_x - obj.x, tip_y - obj.y)
                if dist <= obj.radius + CLAW_TIP_RADIUS:
                    self.attached = obj
                    obj.attached = True
                    if obj.kind == 'tnt':
                        event = 'tnt'  # game detonates it immediately
                    else:
                        event = 'grab'
                    self.state = RETRACT
                    break
            if self.length >= CLAW_MAX_LENGTH:
                self.length = CLAW_MAX_LENGTH
                self.state = RETRACT
                event = event or 'miss'
        elif self.state == RETRACT:
            if self.attached is not None:
                speed = CLAW_RETRACT_BASE_SPEED / self.attached.reel_speed_factor
            else:
                speed = CLAW_RETRACT_EMPTY_SPEED
            self.length -= speed * dt
            if self.length <= CLAW_MIN_LENGTH:
                self.length = CLAW_MIN_LENGTH
                if self.attached is not None:
                    event = 'deliver'  # game banks the object and clears it
                self.state = SWING
        # keep the attached object glued to the claw tip
        if self.attached is not None:
            tx, ty = self.tip()
            self.attached.x = tx
            self.attached.y = ty + self.attached.radius
        return event
    def draw(self, surface):
        """Draw the cable, claw prongs and the pulley."""
        tx, ty = self.tip()
        pygame.draw.line(surface, GRAY_DARK, PIVOT, (tx, ty), 3)
        # claw prongs
        rad = math.radians(self.angle)
        open_ang = math.radians(28)
        for sign in (-1, 1):
            pa = rad + sign * open_ang
            px = tx + math.sin(pa) * 12
            py = ty + math.cos(pa) * 12
            pygame.draw.line(surface, BLACK, (tx, ty), (px, py), 3)
        # pulley
        pygame.draw.circle(surface, BLACK, PIVOT, 8)
        pygame.draw.circle(surface, GRAY_DARK, PIVOT, 8, 2)