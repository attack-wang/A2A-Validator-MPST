'''
The miner's claw: swings, extends, grabs and reels in objects.
State machine: SWING -> EXTEND -> RETRACT -> SWING ...
'''
import math
import pygame
import settings
SWING = 'swing'
EXTEND = 'extend'
RETRACT = 'retract'
class Claw:
    def __init__(self):
        self.pivot = (settings.CLAW_PIVOT_X, settings.CLAW_PIVOT_Y)
        self.angle = 0.0  # degrees, 0 = straight down
        self.swing_dir = 1
        self.state = SWING
        self.length = settings.CLAW_MIN_LENGTH
        self.grabbed = None
        self.tip = self._compute_tip()
    def _compute_tip(self):
        rad = math.radians(self.angle)
        return (self.pivot[0] + math.sin(rad) * self.length,
                self.pivot[1] + math.cos(rad) * self.length)
    def direction(self):
        rad = math.radians(self.angle)
        return (math.sin(rad), math.cos(rad))
    def launch(self):
        """Start extending if the claw is swinging; returns True on success."""
        if self.state == SWING:
            self.state = EXTEND
            return True
        return False
    def update(self, dt, objects, on_grab, on_miss, on_deposit, on_tnt):
        """Advance the claw state machine; game reactions come via callbacks."""
        if self.state == SWING:
            # pendulum motion, bouncing at both angle limits
            self.angle += self.swing_dir * settings.CLAW_SWING_SPEED * dt
            if self.angle >= settings.CLAW_MAX_ANGLE:
                self.angle = settings.CLAW_MAX_ANGLE
                self.swing_dir = -1
            elif self.angle <= settings.CLAW_MIN_ANGLE:
                self.angle = settings.CLAW_MIN_ANGLE
                self.swing_dir = 1
        elif self.state == EXTEND:
            self.length += settings.CLAW_EXTEND_SPEED * dt
            self.tip = self._compute_tip()
            tx, ty = self.tip
            # rope reached the play-area border -> empty retract
            if (tx <= settings.PLAY_AREA_LEFT or tx >= settings.PLAY_AREA_RIGHT
                    or ty >= settings.PLAY_AREA_BOTTOM):
                self.state = RETRACT
                on_miss()
            else:
                # first object whose circle contains the tip is grabbed
                for obj in objects:
                    if obj.alive and obj.collides_with_point(tx, ty, extra=6):
                        self.grabbed = obj
                        obj.alive = False  # removed from the field once caught
                        self.state = RETRACT
                        if isinstance(obj, TNT):
                            # TNT detonates instantly; claw retracts empty
                            self.grabbed = None
                            on_tnt(obj)
                        else:
                            if isinstance(obj, MysteryBag):
                                obj.reveal()  # roll its value now
                            on_grab(obj)
                        break
        elif self.state == RETRACT:
            # heavier objects reel in slower ("takes time to reel in")
            speed = settings.CLAW_RETRACT_SPEED_EMPTY
            if self.grabbed is not None:
                speed /= max(self.grabbed.weight, 0.2)
            self.length -= speed * dt
            if self.grabbed is not None:
                self.tip = self._compute_tip()
                self.grabbed.x, self.grabbed.y = self.tip  # hangs on the claw
            if self.length <= settings.CLAW_MIN_LENGTH:
                self.length = settings.CLAW_MIN_LENGTH
                if self.grabbed is not None:
                    on_deposit(self.grabbed)  # score it
                    self.grabbed = None
                self.state = SWING
        self.tip = self._compute_tip()
    def draw(self, surface):
        """Render the rope, the pivot wheel and the two-pincer claw head."""
        pygame.draw.line(surface, settings.BLACK, self.pivot, self.tip, 3)
        pygame.draw.circle(surface, settings.GRAY, self.pivot, 9)
        pygame.draw.circle(surface, settings.ROCK_DARK, self.pivot, 9, 2)
        tx, ty = self.tip
        rad = math.radians(self.angle)
        # pincers spread wider while swinging, closed while carrying something
        spread = 10 if self.grabbed is None else 4
        for side in (-1, 1):
            px = tx + math.cos(rad) * 10 * side - math.sin(rad) * 6
            py = ty - math.sin(rad) * 10 * side + math.cos(rad) * 6
            pygame.draw.line(surface, settings.ROCK_DARK, (tx, ty), (px, py), 4)
        pygame.draw.circle(surface, settings.YELLOW, (int(tx), int(ty)), 5)