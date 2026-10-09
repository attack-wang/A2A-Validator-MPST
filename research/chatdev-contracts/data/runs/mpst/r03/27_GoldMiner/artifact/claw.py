SWINGING, EXTENDING, RETRACTING = "swinging", "extending", "retracting"
class Claw:
    def __init__(self):
        self.pivot_x, self.pivot_y = PIVOT
        self.angle = 0.0  # radians from straight down
        self.direction = 1
        self.swing_speed = SWING_SPEED_BASE
        self.length = MIN_LENGTH
        self.state = SWINGING
        self.caught = None
        self.min_length = MIN_LENGTH  # rope length at rest, e.g., 40
        self.max_length = MAX_LENGTH  # e.g., distance to bottom corners
    def tip(self):
        return (pivot_x + sin(angle)*length, pivot_y + cos(angle)*length)
    def launch(self):
        if self.state == SWINGING: self.state = EXTENDING
    def update(self, dt, objects):
        if SWINGING: angle += dir*speed*dt; bounce at limits
        elif EXTENDING: length += EXTEND_SPEED*dt; check collisions with objects (tip circle vs object circle); if hit: catch; if length >= max_length or tip out of bounds: state=RETRACTING (empty)
        elif RETRACTING: speed = EMPTY_RETRACT_SPEED if no caught else RETRACT_BASE/caught.weight; length -= speed*dt; if length <= min_length: bank object (return it), state=SWINGING
    def draw(surface): rope line, claw prongs, wheel at pivot; if caught, draw caught object at tip.