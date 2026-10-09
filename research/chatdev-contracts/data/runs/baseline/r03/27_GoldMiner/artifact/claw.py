"""
claw.py
The miner's claw: swings back and forth on a rope, shoots on demand,
grabs an object and reels it in. Heavier objects reel in more slowly,
so every grab costs a different amount of time.
"""
import math
import pygame
import settings as S
SWINGING = 'swinging'
EXTENDING = 'extending'
RETRACTING = 'retracting'
class Claw:
    def __init__(self):
        self.pivot = (S.CLAW_PIVOT_X, S.CLAW_PIVOT_Y)
        self.state = SWINGING
        self.phase = 0.0            # swing phase in radians (0 = straight down)
        self.swing_direction = 1.0  # +1 swinging right, -1 swinging left
        self.swing_speed = S.BASE_SWING_SPEED
        self.length = S.CLAW_MIN_LENGTH
        self.caught = None
        self.launch_angle = 0.0
    @property
    def current_angle(self):
        """Swing angle in radians from straight down."""
        return self.phase
    @property
    def angle_deg(self):
        """Current swing angle in degrees (0 = straight down)."""
        return math.degrees(self.current_angle)
    @property
    def tip(self):
        a = self.launch_angle if self.state != SWINGING else self.current_angle
        return (self.pivot[0] + math.sin(a) * self.length,
                self.pivot[1] + math.cos(a) * self.length)
    def launch(self):
        """Freeze the swing angle and start extending."""
        if self.state == SWINGING:
            self.launch_angle = self.current_angle
            self.state = EXTENDING
    def update(self, dt, objects):
        """Advance one frame: swing → extend → collide → retract by weight."""
        if self.state == SWINGING:
            self.phase += self.swing_direction * self.swing_speed * dt
            amp = math.radians(S.CLAW_SWING_AMPLITUDE)
            if self.phase > amp:
                self.phase = amp
                self.swing_direction = -1.0
            elif self.phase < -amp:
                self.phase = -amp
                self.swing_direction = 1.0
        elif self.state == EXTENDING:
            self.length += S.CLAW_EXTEND_SPEED * dt
            tx, ty = self.tip
            if (tx < 0 or tx > S.SCREEN_WIDTH or ty > S.SCREEN_HEIGHT
                    or self.length > S.CLAW_MAX_LENGTH):
                self.state = RETRACTING
            else:
                for obj in objects:
                    if obj.alive and not obj.caught and obj.hits_point(tx, ty, S.CLAW_TIP_RADIUS):
                        obj.caught = True
                        self.caught = obj
                        self.state = RETRACTING
                        break
        elif self.state == RETRACTING:
            if self.caught is not None:
                speed = S.CLAW_RETRACT_BASE_SPEED / self.caught.weight
            else:
                speed = S.CLAW_RETRACT_EMPTY_SPEED
            self.length -= speed * dt
            if self.length <= S.CLAW_MIN_LENGTH:
                self.length = S.CLAW_MIN_LENGTH
                self.state = SWINGING
                # caller (game.py) resolves the catch when the claw gets home
    def release(self):
        """Detach the caught object (called by the game after resolving it)."""
        self.caught = None
    def draw(self, surface):
        """Draw rope + claw; the caught object hangs at the tip."""
        px, py = self.pivot
        tx, ty = self.tip
        pygame.draw.line(surface, S.ROPE_COLOR, (px, py), (tx, ty), 3)
        # claw body: two pincers around the tip
        a = math.atan2(tx - px, ty - py)  # angle from straight down
        ...