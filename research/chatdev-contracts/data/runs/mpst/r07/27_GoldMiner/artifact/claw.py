'''
claw.py
The miner's claw: swings back and forth, extends on command, grabs objects
and reels them back to the surface. Heavier objects reel in more slowly.
'''
import math
import pygame
import settings
STATE_SWINGING = 'swinging'
STATE_EXTENDING = 'extending'
STATE_REELING = 'reeling'
class Claw:
    def __init__(self):
        self.pivot_x, self.pivot_y = settings.CLAW_PIVOT
        self.angle = 0.0            # degrees, 0 = straight down
        self.direction = 1          # 1 = swinging right, -1 = left
        self.length = settings.CLAW_MIN_LENGTH
        self.state = STATE_SWINGING
        self.caught = None          # GameObject currently attached
        self.swing_speed = settings.CLAW_SWING_SPEED
    def reset(self):
        self.angle = 0.0
        self.direction = 1
        self.length = settings.CLAW_MIN_LENGTH
        self.state = STATE_SWINGING
        self.caught = None
        self.swing_speed = settings.CLAW_SWING_SPEED
    @property
    def tip_position(self):
        rad = math.radians(self.angle)
        tx = self.pivot_x + math.sin(rad) * self.length
        ty = self.pivot_y + math.cos(rad) * self.length
        return tx, ty
    def launch(self):
        if self.state == STATE_SWINGING:
            self.state = STATE_EXTENDING
    def attach(self, obj):
        self.caught = obj
        self.state = STATE_REELING
    def reel_speed(self):
        if self.caught is None:
            return settings.CLAW_RETRACT_SPEED_EMPTY
        return settings.CLAW_BASE_REEL_SPEED / self.caught.weight
    def update(self, dt):
        if self.state == STATE_SWINGING:
            self.angle += self.direction * self.swing_speed * dt
            if self.angle >= settings.CLAW_MAX_ANGLE:
                self.angle = settings.CLAW_MAX_ANGLE
                self.direction = -1
            elif self.angle <= -settings.CLAW_MAX_ANGLE:
                self.angle = -settings.CLAW_MAX_ANGLE
                self.direction = 1
        elif self.state == STATE_EXTENDING:
            self.length += settings.CLAW_EXTEND_SPEED * dt
            if self.length >= settings.CLAW_MAX_LENGTH:
                self.length = settings.CLAW_MAX_LENGTH
                self.state = STATE_REELING  # retract empty
        elif self.state == STATE_REELING:
            self.length -= self.reel_speed() * dt
            if self.length <= settings.CLAW_MIN_LENGTH:
                self.length = settings.CLAW_MIN_LENGTH
                self.state = STATE_SWINGING
                # caller checks claw.caught to deposit
    def draw(self, surface):
        # rope from pivot to tip
        tx, ty = self.tip_position
        pygame.draw.line(surface, settings.ROPE_COLOR,
                         (self.pivot_x, self.pivot_y), (tx, ty), 3)
        # pivot wheel
        pygame.draw.circle(surface, settings.CLAW_DARK_COLOR,
                           (self.pivot_x, self.pivot_y), 8)
        pygame.draw.circle(surface, settings.CLAW_COLOR,
                           (self.pivot_x, self.pivot_y), 5)
        # claw body: two prongs opening along swing direction
        rad = math.radians(self.angle)
        dir_x = math.sin(rad)
        dir_y = math.cos(rad)
        px = -dir_y
        py = dir_x  # perpendicular
        prong_len = 12
        spread = 0.5  # radians-ish offset via perpendicular
        # prong tips
        tip1 = (tx + px * prong_len * 0.8 - dir_x * 2, ty + py * prong_len * 0.8 - dir_y * 2)
        ...