'''
sound.py
Tiny procedural sound manager. Generates simple beeps/noise with the array
module so the game needs no external audio assets. All playback failures
(e.g., no audio device) are swallowed so the game still runs.
'''
import array
import random
import pygame
class SoundManager:
    """Generates and plays simple synthesized sound effects."""
    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate
        self.sounds = {}
        self._enabled = True
        try:
            pygame.mixer.init()
        except pygame.error:
            self._enabled = False  # headless systems: run silently
        if self._enabled:
            self.sounds['shoot'] = self._beep(880, 0.08, 0.25)
            self.sounds['hit'] = self._noise(0.15, 0.3)
            self.sounds['player_hit'] = self._noise(0.4, 0.4)
            self.sounds['bomb'] = self._beep(220, 0.1, 0.2)
    def _beep(self, freq, duration, volume=0.3):
        """Square-ish beep at the given frequency."""
        n = int(self.sample_rate * duration)
        samples = array.array('h')
        for i in range(n):
            s = 1.0 if (i * freq // self.sample_rate) % 2 == 0 else -1.0
            samples.append(int(32767 * volume * s))
        return pygame.mixer.Sound(buffer=samples.tobytes())
    def _noise(self, duration, volume=0.3, decay=True):
        """White-noise burst, optionally decaying (explosion-like)."""
        rate = self.sample_rate
        n = int(rate * duration)
        samples = array.array('h')
        for i in range(n):
            s = random.uniform(-1, 1)
            if decay:
                s *= (1 - i / n)
            samples.append(int(32767 * volume * s))
        return pygame.mixer.Sound(buffer=samples.tobytes())
    def play(self, name):
        """Play a stored sound by name; ignore errors/missing names."""
        if not self._enabled:
            return
        sound = self.sounds.get(name)
        if sound:
            try:
                sound.play()
            except pygame.error:
                pass