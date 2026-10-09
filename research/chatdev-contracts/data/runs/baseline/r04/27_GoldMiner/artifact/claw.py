'''Claw mechanics: swinging, extending, retracting, grabbing.'''
import math
import pygame
from settings import *
SWINGING, EXTENDING, RETRACTING = 'swinging', 'extending', 'retracting'
class Claw:
    def __init__(self, swing_speed):
        self.pivot = (PIVOT_X, PIVOT_Y)
        self.angle = 0.0
        self.angle_speed = swing_speed
        self.dir = 1
        self.length = CLAW_MIN_LENGTH
        self.state = SWINGING
        self.attached = None
        self.min_angle = math.radians(-CLAW_SWING_RANGE_DEG)
        self.max_angle = math.radians(CLAW_SWING_RANGE_DEG)
    def launch(self):
        if self.state == SWINGING:
            self.state = EXTENDING
    def tip(self):
        px, py = self.pivot
        return (px + math.sin(self.angle) * self.length,
                py + math.cos(self.angle) * self.length)
    def attach(self, obj):
        self.attached = obj
        obj.alive = False
        self.state = RETRACTING
    def update_swing(self, dt):
        self.angle += self.dir * self.angle_speed * dt
        if self.angle >= self.max_angle:
            self.angle = self.max_angle
            self.dir = -1
        elif self.angle <= self.min_angle:
            self.angle = self.min_angle
            self.dir = 1
    def extend(self, dt):
        self.length += CLAW_EXTEND_SPEED * dt
    def retract(self, dt):
        speed = CLAW_RETRACT_SPEED_EMPTY if self.attached is None else CLAW_RETRACT_SPEED_EMPTY * 0.55
        self.length -= speed * dt
        if self.length <= CLAW_MIN_LENGTH:
            self.length = CLAW_MIN_LENGTH
            return True
        return False
    def update(self, dt, objects, on_grab, on_tnt):
        """Advance the state machine. Returns events via callbacks."""
        if self.state == SWINGING:
            self.update_swing(dt)
        elif self.state == EXTENDING:
            self.extend(dt)
            tip = self.tip()
            for obj in objects:
                if obj.alive:
                    d = math.hypot(tip[0] - obj.x, tip[1] - obj.y)
                    if d <= obj.radius + CLAW_GRAB_RADIUS:
                        if obj.kind == 'tnt':
                            on_tnt(obj)
                            self.state = RETRACTING
                            return
                        self.attach(obj)
                        on_grab(obj)
                        return
            if self.length >= CLAW_MAX_LENGTH:
                self.state = RETRACTING
        elif self.state == RETRACTING:
            pass  # handled by game loop to allow collection timing