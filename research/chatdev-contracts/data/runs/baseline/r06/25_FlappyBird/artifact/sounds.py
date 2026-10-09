"""
sounds.py
Procedural sound effects (no external audio assets required).
Builds short synthesised tones with pygame.mixer.Sound and exposes
init_sounds() which returns a dict of ready-to-play sounds, or None
when no audio device is available (the game then runs silently).
"""
import array
import math
import random
import pygame
SAMPLE_RATE = 22050
def _tone(duration, freq_start, freq_end, volume=0.5, shape="sine", decay=True):
    """Synthesise a short sweeping tone as a mixer.Sound."""
    n = int(SAMPLE_RATE * duration)
    buf = array.array("h")
    phase = 0.0
    for i in range(n):
        t = i / n
        freq = freq_start + (freq_end - freq_start) * t
        phase += 2 * math.pi * freq / SAMPLE_RATE
        if shape == "sine":
            val = math.sin(phase)
        elif shape == "square":
            val = 1.0 if math.sin(phase) >= 0 else -1.0
        else:  # noise
            val = random.uniform(-1, 1)
        env = (1.0 - t) if decay else 1.0
        buf.append(int(val * env * volume * 32767))
    return pygame.mixer.Sound(buffer=buf.tobytes())
def init_sounds():
    """Initialise the mixer and build every game sound exactly once.
    Must be called before pygame.init() so the mixer uses our sample
    format.  Returns a dict of name -> Sound, or None when audio is
    unavailable so the game can run silently.
    """
    try:
        pygame.mixer.pre_init(SAMPLE_RATE, -16, 1, 512)
        pygame.mixer.init()
    except pygame.error:
        return None
    try:
        return {
            "flap": _tone(0.12, 320, 720, 0.35, "sine"),
            "score": _tone(0.16, 660, 990, 0.35, "sine"),
            "hit": _tone(0.30, 220, 55, 0.45, "square"),
        }
    except pygame.error:
        return None