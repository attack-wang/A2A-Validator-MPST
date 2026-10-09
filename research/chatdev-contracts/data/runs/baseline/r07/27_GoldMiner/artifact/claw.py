'''Claw mechanics: swinging pendulum, extending grab and weighted retraction.'''
import math
import pygame
from settings import *
SWING = 'swinging'
EXTENDING = 'extending'
RETRACTING = 'retracting'
class Claw:
    """The miner's claw. Swings back and forth; the player launches it to grab objects."""
    def __init__(self):
        self.pivot = (PIVOT_X, PIVOT_Y)
        self.min_length = CLAW_MIN_LENGTH
        self.max_length = CLAW_MAX_LENGTH
        self.length = self.min_length
        self.angle = 0.0            # degrees, 0 = straight down
        self.swing_speed = SWING_SPEED
        self.swing_dir = 1
        self.state = SWING
        self.attached = None
        self.retract_speed = BASE_RETRACT_SPEED
    # --- geometry helpers -------------------------------------------------
    def tip(self):
        rad = math.radians(self.angle)
        return (self.pivot[0] + math.sin(rad) * self.length,
                self.pivot[1] + math.cos(rad) * self.length)
    def rope_start(self):
        return self.pivot
    # --- state machine ----------------------------------------------------
    def launch(self):
        """Player action: shoot the claw in the current direction."""
        if self.state == SWING:
            self.state = EXTENDING
    def update(self, objects):
        """Advance the claw one frame. Returns the object collected this frame (or None)."""
        collected = None
        if self.state == SWING:
            self.angle += self.swing_dir * self.swing_speed
            if self.angle >= MAX_ANGLE:
                self.angle = MAX_ANGLE
                self.swing_dir = -1
            elif self.angle <= -MAX_ANGLE:
                self.angle = -MAX_ANGLE
                self.swing_dir = 1
        elif self.state == EXTENDING:
            self.length += EXTEND_SPEED
            tx, ty = self.tip()
            for obj in objects:
                if obj.alive and not obj.being_reeled:
                    dist = math.hypot(tx - obj.x, ty - obj.y)
                    if dist <= obj.collision_radius + 6:
                        self._attach(obj)
                        break
            if self.state == EXTENDING and self.length >= self.max_length:
                self.state = RETRACTING
        elif self.state == RETRACTING:
            if self.attached is not None:
                step = self.retract_speed / self.attached.weight
                self.length -= step
                tx, ty = self.tip()
                self.attached.x = tx
                self.attached.y = ty
                if self.length <= self.min_length:
                    self.length = self.min_length
                    collected = self.attached
                    self.attached = None
                    self.state = SWING
            else:
                self.length -= EMPTY_RETRACT_SPEED
                if self.length <= self.min_length:
                    self.length = self.min_length
                    self.state = SWING
        return collected
    def _attach(self, obj):
        """Grab an object. TNT explodes immediately instead of being reeled in."""
        if obj.type == 'tnt':
            obj.alive = False
            obj.exploded = True   # signal for the game to handle the blast
            self.state = RETRACTING
            self.attached = None
        else:
            obj.being_reeled = True
            self.attached = obj
            self.state = RETRACTING
    def drop(self):
        """Force-release whatever is attached (used on level end / restart)."""
        if self.attached is not None:
            self.attached.being_reeled = False
            self.attached = None
        self.state = SWING
        self.length = self.min_length
        self.angle = 0.0
    # --- rendering ----------------------------------------------------------
    def draw(self, surface):
        tx, ty = self.tip()
        pygame.draw.line(surface, ROPE_COLOR, self.pivot, (tx, ty), 3)
        # pulley wheel at pivot
        pygame.draw.circle(surface, CLAW_COLOR, self.pivot, 8)
        pygame.draw.circle(surface, BLACK, self.pivot, 8, 2)
        # claw: two prongs oriented along the rope direction
        rad = math.radians(self.angle)
        dirx, diry = math.sin(rad), math.cos(rad)
        perp = (diry, -dirx)
        claw_len = 14
        spread = 7
        bx, by = tx, ty
        p1 = (bx + perp[0]*spread, by + perp[1]*spread)
        p2 = (bx - perp[0]*spread, by - perp[1]*spread)
        e1 = (p1[0] + dirx*claw_len - perp[0]*4, p1[1] + diry*claw_len - perp[1]*4)
        e2 = (p2[0] + dirx*claw_len + perp[0]*4, p2[1] + diry*claw_len + perp[1]*4)
        pygame.draw.line(surface, CLAW_COLOR, (bx, by), p1, 4)
        pygame.draw.line(surface, CLAW_COLOR, p1, e1, 4)
        pygame.draw.line(surface, CLAW_COLOR, (bx, by), p2, 4)
        pygame.draw.line(surface, CLAW_COLOR, p2, e2, 4)