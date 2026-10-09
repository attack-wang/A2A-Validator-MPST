'''
Audio module: procedurally generates simple sound effects (no external assets).
'''
import math
import array
import pygame
class Audio:
    """Synthesises all sound effects at runtime so no asset files are needed."""
    def __init__(self):
        self.enabled = False
        self.sounds = {}
        try:
            pygame.mixer.pre_init(22050, -16, 1, 512)
            pygame.mixer.init()
            self.enabled = True
        except pygame.error:
            self.enabled = False
        if self.enabled:
            try:
                self.sounds['flap'] = self._synth(self._flap_fn, 0.18, 0.4)
                self.sounds['score'] = self._synth(self._score_fn, 0.22, 0.4)
                self.sounds['hit'] = self._synth(self._hit_fn, 0.35, 0.5)
            except pygame.error:
                self.enabled = False
                self.sounds = {}
    # ---- waveform generators -------------------------------------------
    @staticmethod
    def _flap_fn(t, p):
        f = 500 + 600 * p
        return math.sin(2 * math.pi * f * t) * (1 - p)
    @staticmethod
    def _score_fn(t, p):
        f = 880 if p < 0.5 else 1320
        return math.sin(2 * math.pi * f * t) * (1 - p * 0.5)
    @staticmethod
    def _hit_fn(t, p):
        f = 300 - 220 * p
        return math.sin(2 * math.pi * f * t) * (1 - p) ** 2
    def _synth(self, gen_fn, duration, volume=0.5):
        """Render a waveform generator into a pygame Sound object."""
        sample_rate = 22050
        n = int(sample_rate * duration)
        buf = array.array('h')
        for i in range(n):
            buf.append(int(volume * 32767 * gen_fn(i / sample_rate, i / n)))
        return pygame.mixer.Sound(buffer=buf.tobytes())
    def play(self, name):
        """Play a named sound if audio is available."""
        if self.enabled and name in self.sounds:
            self.sounds[name].play()