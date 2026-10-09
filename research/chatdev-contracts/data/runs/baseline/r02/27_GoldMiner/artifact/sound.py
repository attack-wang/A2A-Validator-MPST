'''
sound.py
Tiny procedural sound synthesizer (no external assets needed).
'''
import math
import random
import array
import pygame
_mixer_ready = False
_sounds = {}
def init_sounds():
    global _mixer_ready
    try:
        pygame.mixer.init(22050, -16, 1, 512)
        _mixer_ready = True
        _build_sounds()
    except Exception:
        _mixer_ready = False
def _tone(freq, ms, volume=0.5, shape='sine', fade=True):
    rate = 22050
    n = int(rate * ms / 1000)
    buf = array.array('h')
    for i in range(n):
        t = i / rate
        if shape == 'sine':
            s = math.sin(2 * math.pi * freq * t)
        elif shape == 'square':
            s = 1.0 if math.sin(2 * math.pi * freq * t) >= 0 else -1.0
        elif shape == 'noise':
            s = random.uniform(-1, 1)
        else:
            s = math.sin(2 * math.pi * freq * t)
        env = min(1.0, i / (0.01 * rate)) if fade else 1.0
        env *= (1.0 - i / n)
        buf.append(int(s * volume * 32767 * env))
    return pygame.mixer.Sound(buffer=buf.tobytes())