"""
sounds.py
Procedural sound effects generated at runtime (no external assets).
Short waveforms (flap, score, hit, swoosh) are synthesised with the
standard library, converted to the mixer's native 16-bit format and
wrapped in pygame.mixer.Sound. If audio is unavailable the SoundBank
stays empty and the game simply runs silently.
"""
import math
import random
import pygame
SAMPLE_RATE = 22050  # updated at runtime to match the actual mixer init
def _flap_samples():
    """Short airy 'whoosh': noise burst with a falling pitch sweep."""
    length = int(SAMPLE_RATE * 0.12)
    samples = []
    for i in range(length):
        t = i / length
        amplitude = (1.0 - t) * 0.45
        sweep = math.sin(2 * math.pi * (620 - 320 * t) * i / SAMPLE_RATE)
        noise = random.uniform(-1.0, 1.0) * 0.5
        samples.append(amplitude * (sweep * 0.6 + noise * 0.4))
    return samples
def _score_samples():
    """Bright two-tone 'ding-ding' for scoring."""
    length = int(SAMPLE_RATE * 0.22)
    samples = []
    for i in range(length):
        t = i / SAMPLE_RATE
        freq = 880 if i < length // 2 else 1320
        envelope = math.exp(-7 * t)
        samples.append(0.4 * envelope * math.sin(2 * math.pi * freq * t))
    return samples
def _hit_samples():
    """Low descending thud when the bird collides."""
    length = int(SAMPLE_RATE * 0.30)
    samples = []
    for i in range(length):
        t = i / SAMPLE_RATE
        freq = 240 - 170 * (i / length)
        envelope = math.exp(-6 * t)
        samples.append(0.6 * envelope * math.sin(2 * math.pi * freq * t))
    return samples
def _swoosh_samples():
    """Longer falling whistle accompanying the game-over tumble."""
    length = int(SAMPLE_RATE * 0.45)
    samples = []
    for i in range(length):
        t = i / length
        freq = 950 - 700 * t
        envelope = (1.0 - t) * 0.45
        samples.append(envelope * math.sin(2 * math.pi * freq * i / SAMPLE_RATE))
    return samples
def _to_sound(samples):
    """Convert mono floats in [-1, 1] into a pygame.mixer.Sound matching
    the mixer's current format; returns None when unsupported."""
    init = pygame.mixer.get_init()
    if not init:
        return None
    _freq, fmt, channels = init
    if fmt != -16:  # only signed 16-bit output is supported
        return None
    frames = bytearray()
    for sample in samples:
        sample = max(-1.0, min(1.0, sample))
        packed = int(sample * 32000).to_bytes(2, "little", signed=True)
        for _ in range(channels):
            frames += packed
    try:
        return pygame.mixer.Sound(buffer=bytes(frames))
    except pygame.error:
        return None
class SoundBank:
    """Holds generated pygame.mixer.Sound objects, keyed by name."""
    def __init__(self):
        self.sounds = {}
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init(22050, -16, 2, 512)
            init = pygame.mixer.get_init()
            if init:
                global SAMPLE_RATE
                SAMPLE_RATE = init[0]  # generate at the mixer's real rate
                self.sounds = {
                    "flap": _to_sound(_flap_samples()),
                    "score": _to_sound(_score_samples()),
                    "hit": _to_sound(_hit_samples()),
                    "swoosh": _to_sound(_swoosh_samples()),
                }
        except pygame.error:
            self.sounds = {}  # no audio device: run silently
    def play(self, name):
        """Play the named sound if available; ignore silently otherwise."""
        sound = self.sounds.get(name)
        if sound is not None:
            try:
                sound.play()
            except pygame.error:
                pass
def create_sounds():
    """Factory returning a SoundBank; never raises (silent fallback)."""
    try:
        return SoundBank()
    except Exception:
        bank = SoundBank.__new__(SoundBank)
        bank.sounds = {}
        return bank