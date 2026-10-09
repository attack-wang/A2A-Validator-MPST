"""Procedurally generated sound effects (no external assets required)."""
import array
import math
import random
import pygame
class Sounds:
    def __init__(self):
        self.sounds = {}
        self.enabled = False
        try:
            pygame.mixer.init()
            self.enabled = True
        except pygame.error:
            return
        self.sounds["grab"] = self._make_sound(self._tone(660, 0.08, 0.4))
        self.sounds["reel"] = self._make_sound(self._noise(0.15, 0.25))
        self.sounds["score"] = self._make_sound(self._melody([(523, 0.08), (659, 0.08), (784, 0.12)], 0.35))
        self.sounds["boom"] = self._make_sound(self._noise(0.5, 0.6))
        self.sounds["tick"] = self._make_sound(self._tone(880, 0.05, 0.3))
        self.sounds["fail"] = self._make_sound(self._melody([(392, 0.15), (311, 0.2)], 0.4))
        self.sounds["win"] = self._make_sound(self._melody([(523, 0.1), (659, 0.1), (784, 0.1), (1047, 0.2)], 0.4))
    def _to_stereo(self, buf):
        out = array.array("h")
        for s in buf:
            out.append(s)
            out.append(s)
        return out
    def _make_sound(self, buf):
        channels = pygame.mixer.get_init()[2]
        if channels == 2:
            buf = self._to_stereo(buf)
        return pygame.mixer.Sound(buffer=buf.tobytes())
    def _tone(self, frequency, duration, volume=0.5):
        sample_rate = pygame.mixer.get_init()[0]
        n = int(sample_rate * duration)
        buf = array.array("h")
        for t in range(n):
            fade = 1 - t / n
            wave = math.sin(2 * math.pi * frequency * t / sample_rate)
            buf.append(int(volume * 32767 * fade * wave))
        return buf
    def _melody(self, notes, volume=0.5):
        buf = array.array("h")
        for frequency, duration in notes:
            buf.extend(self._tone(frequency, duration, volume))
        return buf
    def _noise(self, duration, volume=0.5):
        sample_rate = pygame.mixer.get_init()[0]
        n = max(1, int(sample_rate * duration))
        buf = array.array("h")
        for i in range(n):
            wave = random.uniform(-1, 1) * (1 - i / n)
            buf.append(int(volume * 32767 * wave))
        return buf
    def play(self, name):
        if self.enabled and name in self.sounds:
            self.sounds[name].play()