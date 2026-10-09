'''Procedurally generated sound effects (no external assets required).'''
import math
import array
import pygame
class SoundManager:
    def __init__(self):
        self.enabled = False
        self.sounds = {}
        try:
            pygame.mixer.init()
            self.enabled = True
        except pygame.error:
            return
        self._build_sounds()
    def _tone(self, start_freq, end_freq, duration, volume=0.5, sample_rate=22050):
        n = int(sample_rate * duration)
        buf = array.array('h')
        phase = 0.0
        for i in range(n):
            t = i / n
            freq = start_freq + (end_freq - start_freq) * t
            phase += 2 * math.pi * freq / sample_rate
            # fade envelope
            env = volume * (1.0 - t) ... 
            sample = int(math.sin(phase) * 32767 * env)
            buf.append(sample)
        return pygame.mixer.Sound(buffer=buf.tobytes())