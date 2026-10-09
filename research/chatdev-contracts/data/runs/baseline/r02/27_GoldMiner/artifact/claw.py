'''
claw.py
The player-controlled claw: swings, extends, grabs, retracts.
'''
import math
import pygame
from settings import (MIN_ROPE_LENGTH, EXTEND_SPEED, RETRACT_SPEED_EMPTY,
                      RETRACT_SPEED_MIN, RETRACT_SPEED_LOADED, CARRY_OFFSET,
                      ROPE_COLOR, CLAW_COLOR, CLAW_DARK)
STATE_SWINGING = 'swinging'
STATE_EXTENDING = 'extending'
STATE_RETRACTING = 'retracting'
class Claw:
    def __init__(self, pivot, min_angle, max_angle, swing_speed):
        self.pivot = pivot
        self.angle = 90.0
        self.direction = 1
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.swing_speed = swing_speed
        self.length = MIN_ROPE_LENGTH
        self.state = STATE_SWINGING
        self.carrying = None
        self.retract_speed = RETRACT_SPEED_EMPTY
    @property
    def tip(self):
        rad = math.radians(self.angle)
        return (self.pivot[0] + math.cos(rad) * self.length,
                self.pivot[1] + math.sin(rad) * self.length)
    def launch(self):
        if self.state == STATE_SWINGING:
            self.state = STATE_EXTENDING
    def attach(self, obj):
        self.carrying = obj
        obj.carried = True
        self.state = STATE_RETRACTING
        self.retract_speed = max(RETRACT_SPEED_MIN, RETRACT_SPEED_LOADED / obj.weight)
    def release(self):
        obj = self.carrying
        self.carrying = None
        self.retract_speed = RETRACT_SPEED_EMPTY
        return obj
    def reset(self):
        self.length = MIN_ROPE_LENGTH
        self.state = STATE_SWINGING
        self.carrying = None
        self.retract_speed = RETRACT_SPEED_EMPTY
        self.angle = 90.0
        self.direction = 1
    def update(self, dt):
        if self.state == STATE_SWINGING:
            self.angle += self.direction * self.swing_speed * dt
            if self.angle >= self.max_angle:
                self.angle = self.max_angle
                self.direction = -1
            elif self.angle <= self.min_angle:
                self.angle = self.min_angle
                self.direction = 1
        elif self.state == STATE_EXTENDING:
            self.length += EXTEND_SPEED * dt
        elif self.state == STATE_RETRACTING:
            self.length -= self.retract_speed * dt
            if self.length <= MIN_ROPE_LENGTH:
                self.length = MIN_ROPE_LENGTH
                self.state = STATE_SWINGING
    def draw(self, surface):
        tip = self.tip
        # rope
        pygame.draw.line(surface, ROPE_COLOR, self.pivot, tip, 3)
        # small pulley wheel at the pivot
        pygame.draw.circle(surface, CLAW_DARK, self.pivot, 8)
        pygame.draw.circle(surface, CLAW_COLOR, self.pivot, 5)
        # carried object hangs just below the claw head
        if self.carrying is not None:
            self.carrying.x = tip[0]
            self.carrying.y = tip[1] + CARRY_OFFSET
            self.carrying.draw(surface)
        # claw head: two prongs opening along the swing direction
        self._draw_claw_head(surface, tip)
    def _draw_claw_head(self, surface, tip):
        rad = math.radians(self.angle)
        # prongs point outward along the rope direction
        spread = 0.45  # radians between prongs
        prong_len = 16
        for sign in (-1, 1):
            a = rad + sign * spread
            end = (tip[0] + math.cos(a) * prong_len,
                   tip[1] + math.sin(a) * prong_len)
            mid = (tip[0] + math.cos(a) * prong_len * 0.5,
                   tip[1] + math.sin(a) * prong_len * 0.5 + 3)
            pygame.draw.line(surface, CLAW_COLOR, tip, mid, 4)
            pygame.draw.line(surface, CLAW_COLOR, mid, end, 4)
        pygame.draw.circle(surface, CLAW_DARK, (int(tip[0]), int(tip[1])), 5)