'''
The player-controlled claw: swings, extends, grabs, and reels in objects.
'''
import math
import pygame
import settings
class Claw:
    SWINGING = "swinging"
    EXTENDING = "extending"
    RETRACTING = "retracting"
    def __init__(self):
        self.pivot_x, self.pivot_y = settings.CLAW_PIVOT
        self.angle = 0.0
        self.direction = 1
        self.state = Claw.SWINGING
        self.length = settings.CLAW_MIN_LENGTH
        self.held_object = None
        self.retract_speed = settings.CLAW_RETRACT_SPEED_EMPTY
        self.events = []  # ("grab", obj) / ("explosion", tnt, destroyed) / ("deliver", obj) / ("miss",)
    @property
    def tip(self):
        tx = self.pivot_x + math.sin(self.angle) * self.length
        ty = self.pivot_y + math.cos(self.angle) * self.length
        return tx, ty
    def launch(self):
        if self.state == Claw.SWINGING:
            self.state = Claw.EXTENDING
    def grab(self, obj, objects):
        '''Attach obj and start retracting. TNT detonates on contact instead.'''
        self.events.append(("grab", obj))
        if obj.kind == "tnt":
            destroyed = obj.explode(objects)
            self.events.append(("explosion", obj, destroyed))
            self.held_object = None
            self.state = Claw.RETRACTING
            self.retract_speed = settings.CLAW_RETRACT_SPEED_EMPTY
        else:
            self.held_object = obj
            obj.alive = False
            self.state = Claw.RETRACTING
            self.retract_speed = settings.CLAW_EXTEND_SPEED / (1 + obj.weight * 0.6)
    def update(self, dt, objects):
        '''Advance the claw one frame; returns the event list for this frame.'''
        self.events = []
        if self.state == Claw.SWINGING:
            self.angle += self.direction * settings.CLAW_SWING_SPEED * dt
            limit = math.radians(settings.CLAW_SWING_ANGLE)
            if self.angle > limit:
                self.angle = limit
                self.direction = -1
            elif self.angle < -limit:
                self.angle = -limit
                self.direction = 1
        elif self.state == Claw.EXTENDING:
            self.length += settings.CLAW_EXTEND_SPEED * dt
            tip = self.tip
            for obj in objects:
                if obj.alive and math.hypot(obj.x - tip[0], obj.y - tip[1]) <= obj.radius + 8:
                    self.grab(obj, objects)
                    break
            if self.state == Claw.EXTENDING and self.length >= settings.CLAW_MAX_LENGTH:
                self.state = Claw.RETRACTING
                self.retract_speed = settings.CLAW_RETRACT_SPEED_EMPTY
                self.events.append(("miss",))
        elif self.state == Claw.RETRACTING:
            self.length -= self.retract_speed * dt
            if self.held_object:
                self.held_object.x, self.held_object.y = self.tip
            if self.length <= settings.CLAW_MIN_LENGTH:
                self.length = settings.CLAW_MIN_LENGTH
                self.state = Claw.SWINGING
                if self.held_object:
                    self.events.append(("deliver", self.held_object))
                    self.held_object = None
        return self.events
    def draw(self, surface):
        # cable
        pygame.draw.line(surface, settings.COLOR_BLACK,
                         (self.pivot_x, self.pivot_y), self.tip, 3)
        # pivot wheel
        pygame.draw.circle(surface, settings.COLOR_DARK_GRAY, (self.pivot_x, self.pivot_y), 10)
        pygame.draw.circle(surface, settings.COLOR_BLACK, (self.pivot_x, self.pivot_y), 10, 2)
        # claw head: two prongs angled from the tip
        tip_x, tip_y = self.tip
        open_amount = 1.0 if self.state != Claw.RETRACTING or self.held_object is None else 0.35
        # Actually simpler: prongs open while swinging/extending, closed while retracting
        spread = 0.5 if self.state != Claw.RETRACTING else 0.15
        for side in (-1, 1):
            a = self.angle + side * spread
            px = tip_x + math.sin(a) * 16
            py = tip_y + math.cos(a) * 16
            pygame.draw.line(surface, settings.COLOR_DARK_GRAY, (tip_x, tip_y), (px, py), 4)
        pygame.draw.circle(surface, settings.COLOR_DARK_GRAY, (int(tip_x), int(tip_y)), 5)