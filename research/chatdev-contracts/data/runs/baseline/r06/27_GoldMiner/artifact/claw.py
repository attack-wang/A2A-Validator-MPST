'''Claw mechanics: pendulum swing, extension, grabbing and reeling.'''
import math
import pygame
from settings import *
SWING, EXTEND, REEL = "swing", "extend", "reel"
class Claw:
    '''The player-controlled claw: swings, extends on input, reels back with loot.'''
    def __init__(self):
        self.pivot = (PIVOT_X, PIVOT_Y)
        self.angle = 0.0
        self.dir = 1
        self.swing_speed = SWING_SPEED
        self.state = SWING
        self.length = MIN_ROPE
        self.held = None
        self.reel_speed = BASE_RETRACT_SPEED
        self.max_length = math.hypot(WIDTH, HEIGHT)
        self.grab_radius = GRAB_RADIUS
        self.events = []  # ("collect", obj) / ("explode", x, y, destroyed)
    def tip(self):
        tx = self.pivot[0] + math.sin(self.angle) * self.length
        ty = self.pivot[1] + math.cos(self.angle) * self.length
        return tx, ty
    def launch(self):
        if self.state == SWING:
            self.state = EXTEND
    def reset(self, swing_speed=None):
        self.angle = 0.0
        self.dir = 1
        self.state = SWING
        self.length = MIN_ROPE
        self.held = None
        self.reel_speed = BASE_RETRACT_SPEED
        self.events = []
        if swing_speed:
            self.swing_speed = swing_speed
    def update(self, dt, level):
        if self.state == SWING:
            self.angle += self.dir * self.swing_speed * dt
            if self.angle > MAX_ANGLE:
                self.angle = MAX_ANGLE
                self.dir = -1
            elif self.angle < -MAX_ANGLE:
                self.angle = -MAX_ANGLE
                self.dir = 1
        elif self.state == EXTEND:
            self.length += EXTEND_SPEED * dt
            tx, ty = self.tip()
            hit = level.object_at(tx, ty, self.grab_radius)
            if hit is not None:
                self.attach(hit, level)
            elif (self.length >= self.max_length or tx < -20 or tx > WIDTH + 20
                  or ty > HEIGHT + 20):
                self.state = REEL
                self.reel_speed = BASE_RETRACT_SPEED
        elif self.state == REEL:
            self.length -= self.reel_speed * dt
            if self.held is not None:
                tx, ty = self.tip()
                self.held.x, self.held.y = tx, ty
            if self.length <= MIN_ROPE:
                self.length = MIN_ROPE
                if self.held is not None:
                    self.events.append(("collect", self.held))
                    self.held = None
                self.state = SWING
    def attach(self, obj, level):
        if obj.kind == "tnt":
            destroyed = level.explode(obj)
            self.events.append(("explode", obj.x, obj.y, destroyed))
            self.held = None
            self.state = REEL
            self.reel_speed = BASE_RETRACT_SPEED * 1.4
            return
        if obj.kind == "mystery":
            obj.resolve_mystery()
        self.held = obj
        obj.alive = False  # removed from field, now attached to the claw
        self.state = REEL
        self.reel_speed = max(90.0, REEL_SPEED / obj.weight)
    def draw(self, surface):
        tx, ty = self.tip()
        pygame.draw.line(surface, ROPE, self.pivot, (tx, ty), 3)
        pygame.draw.circle(surface, ROCK_DARK, self.pivot, 9)
        pygame.draw.circle(surface, ROCK, self.pivot, 5)
        dx, dy = math.sin(self.angle), math.cos(self.angle)
        px, py = math.cos(self.angle), -math.sin(self.angle)
        base = (tx - dx * 4, ty - dy * 4)
        left = (tx + dx * 9 + px * 8, ty + dy * 9 + py * 8)
        right = (tx + dx * 9 - px * 8, ty + dy * 9 - py * 8)
        pygame.draw.lines(surface, ROCK_DARK, False, [left, base, right], 4)
        if self.held is not None:
            self.held.draw(surface)