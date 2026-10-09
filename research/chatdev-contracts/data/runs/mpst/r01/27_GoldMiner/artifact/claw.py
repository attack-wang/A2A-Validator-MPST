"""The miner's claw: swings, extends, grabs objects, and reels them in."""
import math
import pygame
import config
class Claw:
    IDLE = "idle"
    SWINGING = "swinging"
    EXTENDING = "extending"
    RETRACTING = "retracting"
    def __init__(self):
        self.pivot_x = config.CLAW_PIVOT_X
        self.pivot_y = config.CLAW_PIVOT_Y
        self.angle = 0.0
        self.swing_direction = 1
        self.length = 40.0
        self.min_length = 40.0
        self.state = Claw.SWINGING
        self.attached = None
    def tip(self):
        rad = math.radians(self.angle)
        return (
            self.pivot_x + math.sin(rad) * self.length,
            self.pivot_y + math.cos(rad) * self.length,
        )
    def launch(self):
        if self.state == Claw.SWINGING:
            self.state = Claw.EXTENDING
    def attach(self, obj):
        self.attached = obj
        self.state = Claw.RETRACTING
    def update(self, dt, level):
        if self.state == Claw.SWINGING:
            self.angle += self.swing_direction * config.CLAW_SWING_SPEED * dt
            if self.angle >= config.CLAW_MAX_ANGLE:
                self.angle = config.CLAW_MAX_ANGLE
                self.swing_direction = -1
            elif self.angle <= config.CLAW_MIN_ANGLE:
                self.angle = config.CLAW_MIN_ANGLE
                self.swing_direction = 1
        elif self.state == Claw.EXTENDING:
            self.length += config.CLAW_EXTEND_SPEED * dt
            tx, ty = self.tip()
            if (self.length >= config.CLAW_MAX_LENGTH
                    or tx < config.MINING_LEFT or tx > config.MINING_RIGHT
                    or ty > config.MINING_BOTTOM):
                self.state = Claw.RETRACTING
        elif self.state == Claw.RETRACTING:
            speed = config.ROPE_REEL_BASE_SPEED
            if self.attached is not None:
                speed = self.attached.reel_speed(config.ROPE_REEL_BASE_SPEED)
            self.length -= speed * dt
            if self.attached is not None:
                tx, ty = self.tip()
                self.attached.x = tx
                self.attached.y = ty + self.attached.radius * 0.6
            if self.length <= self.min_length:
                self.length = self.min_length
                self.state = Claw.SWINGING
                delivered = self.attached
                self.attached = None
                return delivered
        return None
    def draw(self, surface):
        tx, ty = self.tip()
        pygame.draw.line(surface, config.COLOR_ROPE, (self.pivot_x, self.pivot_y), (tx, ty), 3)
        rad = math.radians(self.angle)
        dirx, diry = math.sin(rad), math.cos(rad)
        open_amount = 10 if self.state == Claw.EXTENDING else 6
        for side in (-1, 1):
            perp_x = math.cos(rad) * side
            perp_y = -math.sin(rad) * side
            base = (tx + perp_x * 3, ty + perp_y * 3)
            end = (tx + dirx * 12 + perp_x * open_amount, ty + diry * 12 + perp_y * open_amount)
            pygame.draw.line(surface, config.COLOR_CLAW, base, end, 4)
        pygame.draw.circle(surface, config.COLOR_CLAW, (int(self.pivot_x), int(self.pivot_y)), 9)
        pygame.draw.circle(surface, config.COLOR_CLAW_DARK, (int(self.pivot_x), int(self.pivot_y)), 9, 2)
        pygame.draw.circle(surface, config.COLOR_CLAW_DARK, (int(self.pivot_x), int(self.pivot_y)), 3)