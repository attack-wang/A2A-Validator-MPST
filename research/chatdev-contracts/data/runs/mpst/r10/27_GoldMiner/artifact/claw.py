"""The player-controlled claw: swinging, extending, grabbing, retracting."""
import math
import random
import pygame
import settings
class Claw:
    """State machine: SWINGING -> EXTENDING -> (grab) -> RETRACTING -> SWINGING."""
    SWINGING, EXTENDING, RETRACTING = "swinging", "extending", "retracting"
    def __init__(self, swing_speed=None):
        self.pivot = (settings.PIVOT_X, settings.PIVOT_Y)
        self.angle = 0.0
        self.swing_direction = 1
        self.swing_speed = swing_speed if swing_speed is not None else 1.5
        self.length = settings.ROPE_MIN_LENGTH
        self.state = self.SWINGING
        self.held = None
        self.just_grabbed = None
        self.just_delivered = None
        self.just_exploded = None
    @property
    def tip(self):
        rad = math.radians(self.angle)
        return (self.pivot[0] + math.sin(rad) * self.length,
                self.pivot[1] + math.cos(rad) * self.length)
    def launch(self):
        if self.state == self.SWINGING:
            self.state = self.EXTENDING
    def update(self, objects):
        """Advance the claw one frame; return a dict of frame events for Game to react to."""
        self.just_grabbed = self.just_delivered = self.just_exploded = None
        if self.state == self.SWINGING:
            self._swing()
        elif self.state == self.EXTENDING:
            self._extend(objects)
        elif self.state == self.RETRACTING:
            self._retract()
        return {"grabbed": self.just_grabbed,
                "delivered": self.just_delivered,
                "exploded": self.just_exploded}
    def _swing(self):
        """Oscillate between -SWING_ANGLE_LIMIT and +SWING_ANGLE_LIMIT."""
        self.angle += self.swing_direction * self.swing_speed
        if abs(self.angle) >= settings.SWING_ANGLE_LIMIT:
            self.angle = math.copysign(settings.SWING_ANGLE_LIMIT, self.angle)
            self.swing_direction *= -1
    def _extend(self, objects):
        """Push the rope out; grab the first object the tip touches."""
        self.length += settings.ROPE_EXTEND_SPEED
        tx, ty = self.tip
        for obj in objects:
            if obj.alive and obj.distance_to(tx, ty) <= obj.radius + 6:
                if obj.kind == "tnt":
                    self.just_exploded = (obj, self._explode(obj, objects))
                    self.state = self.RETRACTING
                else:
                    if obj.kind == "mystery_bag":
                        obj.reveal()
                    self.held = obj
                    obj.alive = False  # removed from field, carried by claw
                    self.just_grabbed = obj
                    self.state = self.RETRACTING
                break
        if self.state == self.EXTENDING:
            if ty >= settings.SCREEN_HEIGHT - 5 or tx <= 0 or tx >= settings.SCREEN_WIDTH:
                self.state = self.RETRACTING  # reached max reach empty
    def _retract(self):
        """Reel in; heavy objects come up slower, delivery happens at the pivot."""
        if self.held is not None:
            speed = max(2.0, settings.RETRACT_BASE_SPEED / self.held.weight)
        else:
            speed = settings.RETRACT_EMPTY_SPEED
        self.length -= speed
        if self.length <= settings.ROPE_MIN_LENGTH:
            self.length = settings.ROPE_MIN_LENGTH
            self.just_delivered = self.held
            self.held = None
            self.state = self.SWINGING
    def _explode(self, tnt, objects):
        """Destroy the TNT and every object within the blast radius."""
        victims = []
        for obj in objects:
            if obj is tnt or not obj.alive:
                continue
            if obj.distance_to(tnt.x, tnt.y) <= settings.TNT_EXPLOSION_RADIUS:
                obj.alive = False
                victims.append(obj)
        tnt.alive = False
        return victims
    def draw(self, surface):
        tx, ty = self.tip
        pygame.draw.line(surface, settings.ROPE_COLOR, self.pivot, (tx, ty), 3)
        self._draw_claw_head(surface, tx, ty)
        if self.held is not None:
            self.held.draw_at(surface, tx, ty + self.held.radius + 8)
    def _draw_claw_head(self, surface, tx, ty):
        rad = math.radians(self.angle)
        # two prongs oriented along the rope direction
        dx = math.sin(rad)
        dy = math.cos(rad)
        px, py = -dy, dx  # perpendicular
        spread = 8
        prong_len = 14
        for side in (-1, 1):
            base = (tx + px * spread * side, ty + py * spread * side)
            end = (base[0] + dx * prong_len + px * 4 * side,
                   base[1] + dy * prong_len + py * 4 * side)
            pygame.draw.line(surface, settings.CLAW_COLOR, base, end, 4)
        pygame.draw.circle(surface, settings.CLAW_DARK, (int(tx), int(ty)), 5)