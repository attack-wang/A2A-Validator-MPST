'''
Procedural sound effects generated at runtime (no external assets).
'''
import array
import math
import random
import pygame
class SoundFactory:
    """Synthesizes simple sound effects with the stdlib (no asset files)."""
    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate
        self.enabled = False
        self.sounds = {}
        try:
            # Re-initialize the mixer with our exact format so the
            # generated samples play at the intended pitch/speed.
            pygame.mixer.quit()
            pygame.mixer.init(frequency=sample_rate, size=-16, channels=1, buffer=512)
            self.enabled = True
        except pygame.error:
            self.enabled = False
    def _tone(self, duration, start_freq, end_freq, volume=0.5, decay=6.0, noise=0.0):
        """Generate a swept sine tone with exponential decay (+ optional noise)."""
        n = int(self.sample_rate * duration)
        samples = []
        phase = 0.0
        for i in range(n):
            t = i / self.sample_rate
            freq = start_freq + (end_freq - start_freq) * (i / n)
            phase += 2 * math.pi * freq / self.sample_rate
            env = math.exp(-decay * t)
            s = math.sin(phase) * env * volume
            if noise:
                s += random.uniform(-noise, noise) * env
            samples.append(s)
        return samples
    def _to_sound(self, samples):
        """Convert float samples (-1..1) into a pygame Sound."""
        clipped = (max(-1.0, min(1.0, s)) for s in samples)
        arr = array.array('h', (int(s * 32767) for s in clipped))
        return pygame.mixer.Sound(buffer=arr.tobytes())
    def build(self):
        """Pre-generate all sound effects."""
        if not self.enabled:
            return
        self.sounds['flap'] = self._to_sound(self._tone(0.12, 350, 700, volume=0.35, decay=18))
        self.sounds['score'] = self._to_sound(
            self._tone(0.09, 880, 880, volume=0.3, decay=10)
            + self._tone(0.12, 1174, 1174, volume=0.3, decay=10))
        self.sounds['hit'] = self._to_sound(
            self._tone(0.3, 220, 60, volume=0.5, decay=8, noise=0.6))
    def play(self, name):
        """Play a named sound if audio is available."""
        if self.enabled and name in self.sounds:
            self.sounds[name].play()