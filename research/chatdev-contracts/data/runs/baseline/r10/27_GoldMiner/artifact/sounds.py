'''
Procedurally generated sound effects (no external audio files needed).
All sounds are synthesized with sine sweeps / noise so the game runs
without any asset dependencies. If the audio mixer is unavailable the
game silently continues without sound.
'''
import array
import math
import random
import pygame
class SoundManager:
    """Builds and plays short procedurally generated sound effects."""
    def __init__(self):
        self.enabled = False
        self.sounds = {}
        try:
            # Mono, 22 kHz so the raw 16-bit buffers below line up exactly.
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            self.enabled = True
        except pygame.error:
            return  # No audio device: keep running silently.
        self.sounds['launch'] = self._make_sweep(300, 900, 0.18, 0.35)
        self.sounds['grab'] = self._make_sweep(900, 500, 0.10, 0.40)
        self.sounds['coin'] = self._make_coin()
        self.sounds['explosion'] = self._make_explosion()
        self.sounds['win'] = self._make_jingle([523, 659, 784, 1047])
        self.sounds['lose'] = self._make_jingle([400, 350, 300, 250])
        self.sounds['tick'] = self._make_sweep(1200, 1200, 0.05, 0.25)
    def _make_sweep(self, start_freq, end_freq, duration, volume=0.4):
        """Return a Sound: a sine whose frequency glides start->end."""
        sample_rate = 22050
        n = int(sample_rate * duration)
        buf = array.array('h')
        phase = 0.0
        for i in range(n):
            t = i / n
            freq = start_freq + (end_freq - start_freq) * t
            phase += 2 * math.pi * freq / sample_rate
            env = 1.0 - t  # linear fade-out envelope
            sample = int(volume * env * 32767 * math.sin(phase))
            buf.append(sample)
        try:
            return pygame.mixer.Sound(buffer=buf.tobytes())
        except Exception:
            return None
    def _make_coin(self, duration=0.22, volume=0.4):
        """Classic two-note 'coin' blip (B5 -> E6)."""
        sample_rate = 22050
        n = int(sample_rate * duration)
        buf = array.array('h')
        half = n // 2
        for i in range(n):
            freq = 988 if i < half else 1319
            t = (i % half) / half
            env = 1.0 - t
            sample = int(volume * env * 32767 * math.sin(2 * math.pi * freq * i / sample_rate))
            buf.append(sample)
        try:
            return pygame.mixer.Sound(buffer=buf.tobytes())
        except Exception:
            return None
    def _make_explosion(self, duration=0.5, volume=0.5):
        """Filtered white-noise burst with a decaying envelope."""
        sample_rate = 22050
        n = int(sample_rate * duration)
        buf = array.array('h')
        value = 0.0
        for i in range(n):
            t = i / n
            env = (1.0 - t) ** 2
            value = 0.92 * value + 0.08 * random.uniform(-1, 1)  # low-pass noise
            sample = int(volume * env * 32767 * value * 3)
            # clamp to 16-bit range
            sample = max(-32768, min(32767, sample))
            buf.append(sample)
        try:
            return pygame.mixer.Sound(buffer=buf.tobytes())
        except Exception:
            return None
    def _make_jingle(self, notes, note_len=0.14, volume=0.35):
        """Play a short sequence of sine notes one after another."""
        sample_rate = 22050
        buf = array.array('h')
        for freq in notes:
            n = int(sample_rate * note_len)
            for i in range(n):
                t = i / n
                env = 1.0 - t
                sample = int(volume * env * 32767 * math.sin(2 * math.pi * freq * i / sample_rate))
                buf.append(sample)
        try:
            return pygame.mixer.Sound(buffer=buf.tobytes())
        except Exception:
            return None
    def play(self, name):
        """Play a stored sound by key; no-op when audio is disabled."""
        if self.enabled and name in self.sounds and self.sounds[name] is not None:
            self.sounds[name].play()