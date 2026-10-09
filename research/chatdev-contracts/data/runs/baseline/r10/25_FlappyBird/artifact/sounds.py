'''
sounds.py
Procedurally generated sound effects (no external audio assets needed).
Creates simple decaying sine-wave tones for flap, score and hit events.
Silently degrades to no-ops when the audio mixer is unavailable.
Fix applied from the test report: the tone buffer is now interleaved for
stereo mixers, so pitch/duration stay correct when the audio driver forces
channels=2 instead of the requested mono layout.
'''
import math
import array
import pygame
def _make_tone(frequency, duration, volume=0.5):
    """Generate a decaying sine-wave tone as a pygame Sound (stereo-aware)."""
    mixer_init = pygame.mixer.get_init()
    if mixer_init is None:
        return None
    sample_rate, _format, channels = mixer_init
    n = int(sample_rate * duration)
    mono = array.array(
        'h',
        (int(32767 * volume * math.sin(2 * math.pi * frequency * i / sample_rate) * (1 - i / n))
         for i in range(n))
    )
    if channels == 2:
        buf = array.array('h')
        for sample in mono:
            buf.append(sample)
            buf.append(sample)
    else:
        buf = mono
    return pygame.mixer.Sound(buffer=buf.tobytes())
def create_sounds():
    """Return a dict of sound effects, or an empty dict if audio fails."""
    try:
        if pygame.mixer.get_init() is None:
            pygame.mixer.init()
        sounds = {
            "flap": _make_tone(520, 0.12, 0.4),
            "point": _make_tone(880, 0.18, 0.45),
            "hit": _make_tone(160, 0.35, 0.6),
        }
        return {name: snd for name, snd in sounds.items() if snd is not None}
    except pygame.error:
        return {}