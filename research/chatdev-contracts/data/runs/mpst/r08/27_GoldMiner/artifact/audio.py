'''Simple synthesized sound effects (optional; requires numpy).'''
import pygame
try:
    import numpy as np
    _HAS_NUMPY = True
except ImportError:
    _HAS_NUMPY = False
_SAMPLE_RATE = 22050
def _tone(freq, duration, volume=0.5, shape='sine'):
    """Build a simple enveloped tone as a stereo pygame Sound."""
    t = np.linspace(0, duration, int(_SAMPLE_RATE * duration), False)
    envelope = np.minimum(1.0, np.minimum(t / 0.01, (duration - t) / 0.05))
    envelope = np.clip(envelope, 0.0, 1.0)
    if shape == 'sine':
        wave = np.sin(freq * 2 * np.pi * t) * envelope
    elif shape == 'square':
        wave = np.sign(np.sin(freq * 2 * np.pi * t)) * envelope * 0.6
    else:  # noise
        wave = (np.random.uniform(-1, 1, len(t))) * envelope
    array = np.array(wave * 32768 * volume, dtype=np.int16)
    stereo = np.column_stack((array, array))
    return pygame.sndarray.make_sound(np.ascontiguousarray(stereo))
def init_sounds():
    """Return a dict of sound effects, or None if numpy is unavailable."""
    if not _HAS_NUMPY:
        return None
    try:
        return {
            'grab':   _tone(660, 0.12, 0.4),
            'deliver': _tone(880, 0.18, 0.5),
            'miss':   _tone(180, 0.15, 0.4),
            'boom':   _tone(0, 0.4, 0.6, shape='noise'),
            'click':  _tone(440, 0.08, 0.3),
            'tick':   _tone(1200, 0.05, 0.25),
        }
    except Exception:
        return None
def play(sounds, name):
    """Safely play a named sound if the sound set exists."""
    if sounds and name in sounds:
        try:
            sounds[name].play()
        except Exception:
            pass