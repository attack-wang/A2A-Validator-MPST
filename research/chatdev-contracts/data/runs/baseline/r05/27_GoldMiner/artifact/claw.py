"""Claw mechanics: swinging, extending, grabbing, reeling."""
import math
import pygame
from config import *
from objects import GameObject
SWINGING = "swinging"
EXTENDING = "extending"
REELING = "reeling"       # reeling with an attached object
RETRACTING = "retracting" # empty retract
class Claw:
    def __init__(self):
        self.pivot = (CLAW_PIVOT_X, CLAW_PIVOT_Y)
        self.angle = 0.0            # degrees from straight down
        self.swing_dir = 1
        self.length = CLAW_MIN_LENGTH
        self.state = SWINGING
        self.attached = None        # GameObject being reeled in
        self.swing_phase = 0.0      # radians
        self.explosion_callback = None  # set by game to handle TNT
    def tip_position(self):
        rad = math.radians(self.angle)
        x = self.pivot[0] + math.sin(rad) * self.length
        y = self.pivot[1] + math.cos(rad) * self.length
        return (x, y)
    def launch(self):
        if self.state == SWINGING:
            self.state = EXTENDING
    def update(self, dt, objects):
        """Advance claw state machine. Returns list of events."""
        events = []
        if self.state == SWINGING:
            self.swing_phase += CLAW_SWING_SPEED * dt
            self.angle = CLAW_SWING_AMPLITUDE * math.sin(self.swing_phase)
        elif self.state == EXTENDING:
            self.length += CLAW_EXTEND_SPEED * dt
            tip = self.tip_position()
            # check bounds
            if tip[0] < 0 or tip[0] > SCREEN_WIDTH or tip[1] > SCREEN_HEIGHT - STATUS_BAR_HEIGHT or self.length > CLAW_MAX_LENGTH:
                self.state = RETRACTING
            else:
                # check object collisions
                for obj in objects:
                    if obj.alive and distance(tip, obj.position) <= obj.radius + 6:
                        self._grab(obj)
                        events.append(("grab", obj))
                        break
        elif self.state == REELING:
            speed = CLAW_RETRACT_BASE_SPEED / max(1, self.attached.weight)
            self.length -= speed * dt
            # move object with tip
            tip = self.tip_position()
            self.attached.x = tip[0]
            self.attached.y = tip[1] + self.attached.radius  # hang below claw
            if self.length <= CLAW_MIN_LENGTH:
                self.length = CLAW_MIN_LENGTH
                events.append(("delivered", self.attached))
                self.attached = None
                self.state = SWINGING
        elif self.state == RETRACTING:
            self.length -= CLAW_RETRACT_EMPTY_SPEED * dt
            if self.length <= CLAW_MIN_LENGTH:
                self.length = CLAW_MIN_LENGTH
                self.state = SWINGING
        return events
    def _grab(self, obj):
        if obj.kind == "tnt":
            # explode: handled via event; claw retracts empty
            self.state = RETRACTING
            # mark tnt for explosion via event
        else:
            self.attached = obj
            obj.alive = False  # hmm, careful: if not alive it won't be drawn/updated? We still need to draw it while attached.
            self.state = REELING