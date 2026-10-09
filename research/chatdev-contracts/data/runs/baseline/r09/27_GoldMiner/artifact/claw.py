import math
import pygame
from settings import *
SWING, EXTEND, RETRACT = "swing", "extend", "retract"
class Claw:
    def __init__(self):
        self.reset()
    def reset(self):
        self.angle = 0.0
        self.direction = 1
        self.length = ROPE_IDLE
        self.state = SWING
        self.grabbed = None
    def swing_speed(self, level):
        return min(SWING_SPEED_MAX, SWING_SPEED_BASE + SWING_SPEED_PER_LEVEL * (level - 1))
    def launch(self):
        if self.state == SWING:
            self.state = EXTEND
    def tip_position(self):
        rad = math.radians(self.angle)
        return (PIVOT_X + math.sin(rad) * self.length,
                PIVOT_Y + math.cos(rad) * self.length)
    def update(self, dt, level, objects, on_grab, on_collect, on_tnt):
        if self.state == SWING:
            speed = self.swing_speed(level.number)
            self.angle += self.direction * speed * dt
            if self.angle >= MAX_ANGLE:
                self.angle = MAX_ANGLE; self.direction = -1
            elif self.angle <= -MAX_ANGLE:
                self.angle = -MAX_ANGLE; self.direction = 1
        elif self.state == EXTEND:
            self.length += EXTEND_SPEED * dt
            tip = self.tip_position()
            for obj in objects:
                if obj.alive and not obj.grabbed:
                    if obj.distance_to(*tip) <= obj.radius + CLAW_SIZE * 0.5:
                        if obj.kind == "tnt":
                            obj.alive = False
                            self.grabbed = None
                            self.state = RETRACT
                            on_tnt(obj)
                        else:
                            obj.grabbed = True
                            self.grabbed = obj
                            self.state = RETRACT
                            on_grab(obj)
                        break
            if self.state == EXTEND and self.length >= MAX_ROPE:
                self.state = RETRACT
        elif self.state == RETRACT:
            if self.grabbed is not None:
                speed = BASE_REEL_SPEED / max(0.3, self.grabbed.weight)
            else:
                speed = EMPTY_RETRACT_SPEED
            self.length -= speed * dt
            if self.length <= ROPE_IDLE:
                self.length = ROPE_IDLE
                if self.grabbed is not None:
                    obj, self.grabbed = self.grabbed, None
                    obj.grabbed = False
                    obj.alive = False
                    on_collect(obj)
                self.state = SWING
        # keep grabbed object glued to the claw tip
        if self.grabbed is not None:
            tip = self.tip_position()
            self.grabbed.x, self.grabbed.y = tip