"""Sound synthesis and playback with graceful fallbacks."""
import pygame
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    np = None
    NUMPY_AVAILABLE = False
SAMPLE_RATE = 22050
class _DummySound:
    """No-op stand-in used when audio is unavailable."""
    def play(self):
        pass
class SoundManager:
    """Builds simple synthesized effects; degrades to silence on failure."""
    def __init__(self):
        self.enabled = False
        self.sounds = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.pre_init(SAMPLE_RATE, -16, 2, 512)
                pygame.mixer.init()
            if NUMPY_AVAILABLE and pygame.mixer.get_init():
                self.sounds = {
                    "flap": self._make_sound(self._flap_wave()),
                    "score": self._make_sound(self._score_wave()),
                    "hit": self._make_sound(self._hit_wave()),
                }
                self.enabled = True
        except Exception:
            self.sounds = {}
            self.enabled = False
    def _make_sound(self, arr):
        """Convert a float waveform in [-1, 1] to a pygame Sound."""
        arr = np.clip(arr, -1.0, 1.0)
        pcm = (arr * 32767.0).astype(np.int16)
        stereo = np.column_stack((pcm, pcm))
        return pygame.sndarray.make_sound(np.ascontiguousarray(stereo))
    def _flap_wave(self):
        """Short rising whoosh."""
        duration = 0.12
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        freq = 300 + 500 * (t / duration)
        wave = np.sin(2 * np.pi * np.cumsum(freq) / SAMPLE_RATE)
        envelope = np.exp(-t * 18)
        return wave * envelope * 0.5
    def _score_wave(self):
        """Bright two-tone ding."""
        duration = 0.18
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        wave = np.sin(2 * np.pi * 880 * t) + 0.5 * np.sin(2 * np.pi * 1320 * t)
        envelope = np.exp(-t * 14)
        return wave * envelope * 0.35
    def _hit_wave(self):
        """Low thud with noise burst."""
        duration = 0.3
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        wave = np.sin(2 * np.pi * 120 * t) * np.exp(-t * 10)
        noise = np.random.uniform(-1, 1, len(t)) * np.exp(-t * 25) * 0.4
        return (wave + noise) * 0.6
    def play(self, name):
        """Play a named sound if audio is available."""
        if self.enabled:
            sound = self.sounds.get(name)
            if sound:
                sound.play()