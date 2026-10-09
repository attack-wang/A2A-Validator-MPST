"""
input_handler.py
Key-repeat helper: supports DAS-style auto-repeat for held movement keys.
"""
class InputRepeater:
    """Handles key repeat for held movement keys."""
    def __init__(self, delay=0.17, interval=0.05):
        """Create a repeater with the given initial delay and repeat interval."""
        self.delay = delay
        self.interval = interval
        self.keys = {}  # key -> [held_time, time_since_last_repeat]
    def press(self, key):
        """Register a key press, starting its repeat timer."""
        self.keys[key] = [0.0, 0.0]
    def release(self, key):
        """Forget a key release, stopping its repeat timer."""
        self.keys.pop(key, None)
    def update(self, dt):
        """Return the list of keys that should trigger a repeat this frame."""
        repeats = []
        for key, state in self.keys.items():
            state[0] += dt
            state[1] += dt
            if state[0] >= self.delay and state[1] >= self.interval:
                state[1] = 0.0
                repeats.append(key)
        return repeats