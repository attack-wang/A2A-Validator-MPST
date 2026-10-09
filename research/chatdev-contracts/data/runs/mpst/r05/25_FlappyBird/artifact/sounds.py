'''Procedurally synthesized sound effects (no audio files required).'''
import math
import array
import pygame
def make_sound(frequency, duration, volume=0.5, shape="square"):
    """Synthesize a short tone as a mixer Sound (16-bit mono)."""
    sample_rate = 22050
    n = max(1, int(sample_rate * duration))
    buf = array.array("h", (0 for _ in range(n)))
    if buf.itemsize != 2:
        raise pygame.error("16-bit samples unsupported on this platform")
    for i in range(n):
        t = i / sample_rate
        if shape == "square":
            v = 1.0 if math.sin(2.0 * math.pi * frequency * t) >= 0.0 else -1.0
        else:
            v = math.sin(2.0 * math.pi * frequency * t)
        envelope = 1.0 - (i / n)  # linear decay so the tone fades out
        buf[i] = int(32767 * volume * v * envelope)
    return pygame.mixer.Sound(buffer=buf.tobytes())
def build_sounds():
    """Initialize the mixer and build all game sounds; returns {} on failure."""
    sounds = {}
    try:
        pygame.mixer.pre_init(22050, -16, 1, 512)  # mono 16-bit for generated buffers
        pygame.mixer.init()
        sounds["flap"] = make_sound(500, 0.10, 0.4, "square")
        sounds["score"] = make_sound(880, 0.12, 0.35, "sine")
        sounds["hit"] = make_sound(180, 0.25, 0.5, "square")
        sounds["die"] = make_sound(120, 0.40, 0.5, "sine")
    except pygame.error:
        sounds = {}
    return sounds