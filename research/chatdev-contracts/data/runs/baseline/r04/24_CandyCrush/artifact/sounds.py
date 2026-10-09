'''
sounds.py
Procedural sound effects generated with the pygame mixer so the game runs
even on systems without audio devices (all failures are silently ignored).
'''
import math
import struct
import pygame
SAMPLE_RATE = 22050
def _tone(freq, duration, amplitude=0.35, decay=True):
    """Build a simple synthesized tone as an SDL sound buffer."""
    n = int(SAMPLE_RATE * duration)
    buf = bytearray()
    for t in range(n):
        wave = math.sin(2 * math.pi * freq * t / SAMPLE_RATE)
        if decay:
            wave *= 1.0 - (t / n)  # linear fade-out
        buf += struct.pack('<h', int(amplitude * wave * 32767))
    return pygame.mixer.Sound(buffer=bytes(buf))
class Sounds:
    """Container of generated sound effects; no-ops when audio is unavailable."""
    def __init__(self):
        self.enabled = False
        self.swap = None
        self.invalid = None
        self.match = None
        self.combo = None
        self.win = None
        self.lose = None
        try:
            pygame.mixer.init()
        except pygame.error:
            return  # no audio device: keep sounds disabled
        try:
            self.swap = _tone(440, 0.08, 0.25)
            self.invalid = _tone(160, 0.18, 0.30)
            self.match = _tone(660, 0.15, 0.30)
            self.combo = _tone(880, 0.20, 0.30)
            self.win = _tone(990, 0.5, 0.30)
            self.lose = _tone(180, 0.6, 0.30)
            self.enabled = True
        except pygame.error:
            self.enabled = False
    def play(self, name):
        """Play a named effect if audio is available."""
        if not self.enabled:
            return
        sound = getattr(self, name, None)
        if sound is not None:
            try:
                sound.play()
            except pygame.error:
                pass