"""Claw mechanics: swinging pendulum, extending rope, retracting with cargo."""
import math
import pygame
import settings
class Claw:
    SWINGING = "swinging"
    EXTENDING = "extending"
    RETRACTING = "retracting"
    def __init__(self):
        self.pivot = (settings.CLAW_PIVOT_X, settings.CLAW_PIVOT_Y)
        self.angle = 0.0
        self.direction = 1
        self.length = settings.CLAW_MIN_LENGTH
        self.state = self.SWINGING
        self.grabbed = None
        self.flash_timer = 0.0
    @property
    def tip(self):
        rad = math.radians(self.angle)
        return (self.pivot[0] + math.sin(rad) * self.length,
                self.pivot[1] + math.cos(rad) * self.length)
    def launch(self):
        if self.state == self.SWINGING:
            self.state = self.EXTENDING
    def update(self, dt, objects):
        """Advance claw state machine. Returns list of event tuples."""
        events = []
        if self.flash_timer > 0:
            self.flash_timer -= dt
        if self.state == self.SWINGING:
            self.angle += self.direction * settings.CLAW_SWING_SPEED * dt
            if self.angle > settings.CLAW_MAX_ANGLE:
                self.angle = settings.CLAW_MAX_ANGLE
                self.direction = -1
            elif self.angle < -settings.CLAW_MAX_ANGLE:
                self.angle = -settings.CLAW_MAX_ANGLE
                self.direction = 1
        elif self.state == self.EXTENDING:
            self.length += settings.CLAW_EXTEND_SPEED * dt
            tip = self.tip
            for obj in objects:
                if not obj.alive:
                    continue
                dist = math.hypot(obj.x - tip[0], obj.y - tip[1])
                if dist <= obj.radius + settings.CLAW_RADIUS:
                    if obj.kind == "tnt":
                        obj.alive = False
                        events.append(("explode", obj))
                        self.flash_timer = 0.3
                        self.state = self.RETRACTING
                    else:
                        self.grabbed = obj
                        obj.alive = False
                        events.append(("grab", obj))
                        self.state = self.RETRACTING
                    break
            if self.state == self.EXTENDING and self.length >= settings.CLAW_MAX_LENGTH:
                self.state = self.RETRACTING
        elif self.state == self.RETRACTING:
            weight = self.grabbed.weight if self.grabbed else 1.0
            speed = settings.CLAW_RETRACT_BASE_SPEED / weight
            self.length -= speed * dt
            if self.grabbed:
                self.grabbed.x, self.grabbed.y = self.tip
            if self.length <= settings.CLAW_MIN_LENGTH:
                self.length = settings.CLAW_MIN_LENGTH
                if self.grabbed:
                    events.append(("deposit", self.grabbed))
                    self.grabbed = None
                self.state = self.SWINGING
        return events
    def draw(self, surface):
        # rope
        pygame.draw.line(surface, settings.COLOR_ROPE, self.pivot, self.tip, 3)
        # pulley
        pygame.draw.circle(surface, settings.COLOR_CLAW, self.pivot, 10)
        pygame.draw.circle(surface, settings.COLOR_BLACK, self.pivot, 10, 2)
        # claw head
        tip = self.tip
        pygame.draw.circle(surface, settings.COLOR_CLAW, (int(tip[0]), int(tip[1])), 8)
        # prongs
        rad = math.radians(self.angle)
        px, py = math.cos(rad), -math.sin(rad)
        open_amount = 12 if self.grabbed is None else 6
        for side in (-1, 1):
            bx = tip[0] + px * side * open_amount
            by = tip[1] + py * side * open_amount
            ex = tip[0] + math.sin(rad) * 16 + px * side * (open_amount - 6)
            ey = tip[1] + math.cos(rad) * 16 + py * side * (open_amount - 6)
            pygame.draw.line(surface, settings.COLOR_CLAW, (bx, by), (ex, ey), 4)
        # explosion flash
        if self.flash_timer > 0:
            pygame.draw.circle(surface, settings.COLOR_ORANGE, (int(tip[0]), int(tip[1])), 20, 3)