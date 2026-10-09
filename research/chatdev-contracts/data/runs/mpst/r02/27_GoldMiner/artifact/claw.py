'''
claw.py
The player-controlled mining claw.
Swings back and forth on a rope, extends when launched, grabs the first
object its tip touches, then reels the object back (heavier = slower).
'''
import math
import pygame
import settings
class Claw:
    STATE_SWINGING = "swinging"
    STATE_EXTENDING = "extending"
    STATE_RETRACTING = "retracting"
    def __init__(self, swing_speed=1.6):
        self.pivot_x = settings.PIVOT_X
        self.pivot_y = settings.PIVOT_Y
        self.angle = 90.0
        self.direction = 1
        self.swing_speed = swing_speed
        self.length = settings.CLAW_MIN_LENGTH
        self.state = self.STATE_SWINGING
        self.caught = None
        self.extend_speed = settings.CLAW_EXTEND_SPEED
        self.retract_speed = settings.CLAW_RETRACT_EMPTY_SPEED
    @property
    def tip_x(self):
        return self.pivot_x + math.cos(math.radians(self.angle)) * self.length
    @property
    def tip_y(self):
        return self.pivot_y + math.sin(math.radians(self.angle)) * self.length
    def launch(self):
        """Shoot the claw out; only allowed while it is swinging."""
        if self.state == self.STATE_SWINGING:
            self.state = self.STATE_EXTENDING
    def update(self, level_objects):
        """Advance claw physics. Returns the object delivered this frame (or None)."""
        delivered = None
        if self.state == self.STATE_SWINGING:
            self.angle += self.swing_speed * self.direction
            if self.angle >= settings.CLAW_MAX_ANGLE:
                self.angle = settings.CLAW_MAX_ANGLE
                self.direction = -1
            elif self.angle <= settings.CLAW_MIN_ANGLE:
                self.angle = settings.CLAW_MIN_ANGLE
                self.direction = 1
        elif self.state == self.STATE_EXTENDING:
            self.length += self.extend_speed
            tx, ty = self.tip_x, self.tip_y
            # grab check: tip within (radius + grab radius) of an object centre
            for obj in level_objects:
                if obj.contains_point(tx, ty, extra=settings.CLAW_GRAB_RADIUS):
                    self.caught = obj
                    level_objects.remove(obj)
                    self.state = self.STATE_RETRACTING
                    # weight is guaranteed >= 1.0 in settings.OBJECT_STATS,
                    # so a loaded claw ALWAYS reels in slower than an empty one
                    self.retract_speed = settings.CLAW_RETRACT_EMPTY_SPEED / obj.weight
                    break
            else:
                # nothing grabbed: stop at max length or screen borders
                if (self.length >= settings.CLAW_MAX_LENGTH
                        or tx < 0 or tx > settings.SCREEN_WIDTH
                        or ty > settings.SCREEN_HEIGHT - 4):
                    self.state = self.STATE_RETRACTING
                    self.retract_speed = settings.CLAW_RETRACT_EMPTY_SPEED
        elif self.state == self.STATE_RETRACTING:
            self.length -= self.retract_speed
            if self.caught is not None:
                # keep the caught object glued to the claw tip so its
                # on-screen position updates every frame during reel-in
                self.caught.x = self.tip_x
                self.caught.y = self.tip_y
            if self.length <= settings.CLAW_MIN_LENGTH:
                self.length = settings.CLAW_MIN_LENGTH
                delivered = self.caught
                self.caught = None
                self.state = self.STATE_SWINGING
        return delivered
    def draw(self, surface):
        px, py = int(self.pivot_x), int(self.pivot_y)
        tx, ty = int(self.tip_x), int(self.tip_y)
        # rope
        pygame.draw.line(surface, settings.ROPE_COLOR, (px, py), (tx, ty), 3)
        # pulley wheel at the pivot
        pygame.draw.circle(surface, settings.CLAW_COLOR, (px, py), 9)
        pygame.draw.circle(surface, settings.BLACK, (px, py), 9, 2)
        pygame.draw.circle(surface, settings.BLACK, (px, py), 3)
        # claw head: two prongs splay forward; they close when holding cargo
        spread = 10 if self.caught is not None else 28
        base = math.radians(self.angle)
        for sign in (-1, 1):
            pa = base + sign * math.radians(spread)
            ex = tx + math.cos(pa) * 15
            ey = ty + math.sin(pa) * 15
            pygame.draw.line(surface, settings.CLAW_COLOR, (tx, ty), (ex, ey), 4)
        pygame.draw.circle(surface, settings.CLAW_COLOR, (tx, ty), 5)