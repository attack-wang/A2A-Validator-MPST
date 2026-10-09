'''
sounds.py
Procedurally generated sound effects (no external assets needed).
Every effect is synthesised at runtime with the standard library
(array + math) and wrapped in pygame.mixer.Sound objects, so the game
ships without any audio files.  Four effects are provided:
    flap  - short rising square blip played when the bird flaps
    point - bright two-tone chime played when a pipe is passed
    hit   - dull falling triangle thud played on collision
    fall  - long descending whistle played while the bird tumbles
If the audio device cannot be initialised (no sound card, SDL mixer
unavailable, ...) every function degrades gracefully: init() returns
False and play() becomes a silent no-op, keeping the game fully
playable without sound.
'''
import array
import math
import pygame
_SAMPLE_RATE = 22050
_sounds = {}
def _synth(freq_start, freq_end, duration, volume=0.4, shape="sine"):
    """Synthesise a frequency-sweep tone with fade in/out envelope.
    Generates `duration` seconds of mono signed-16-bit audio at
    _SAMPLE_RATE, sweeping the frequency linearly from freq_start to
    freq_end.  `shape` selects the oscillator waveform: "sine",
    "square" or "triangle".  Returns raw bytes ready for
    pygame.mixer.Sound(buffer=...).
    """
    n = int(_SAMPLE_RATE * duration)
    samples = array.array("h", bytes(2 * n))
    fade = max(1, int(0.03 * _SAMPLE_RATE))
    phase = 0.0
    for i in range(n):
        # Linear frequency sweep; accumulate the phase so the sweep
        # stays continuous and free of discontinuity artifacts.
        f = freq_start + (freq_end - freq_start) * (i / n)
        phase += 2.0 * math.pi * f / _SAMPLE_RATE
        if shape == "square":
            wave = 1.0 if math.sin(phase) >= 0 else -1.0
        elif shape == "triangle":
            wave = 2.0 / math.pi * math.asin(math.sin(phase))
        else:
            wave = math.sin(phase)
        # Linear fade-in/out envelope (~30 ms) to avoid clicks/pops.
        envelope = 1.0
        if i < fade:
            envelope = i / fade
        elif n - i < fade:
            envelope = (n - i) / fade
        value = volume * envelope * wave
        # Clamp to the signed-16-bit range for safety.
        value = max(-1.0, min(1.0, value))
        samples[i] = int(value * 32767)
    return samples.tobytes()
def _ding():
    """Two-tone 'point' chime (880 Hz blip into a 1320 Hz ring)."""
    part1 = _synth(880, 880, 0.08, 0.35, "sine")
    part2 = _synth(1320, 1320, 0.12, 0.35, "sine")
    return part1 + part2
def init():
    """Initialise the mixer and pre-generate every sound effect.
    Returns True when audio is available, False otherwise (the game
    must keep running silently in that case).
    """
    global _sounds
    try:
        # Start from a clean slate if a mixer is already open.
        if pygame.mixer.get_init() is not None:
            pygame.mixer.quit()
        pygame.mixer.init(frequency=_SAMPLE_RATE, size=-16, channels=1, buffer=512)
    except pygame.error:
        _sounds = {}
        return False
    try:
        _sounds = {
            "flap": pygame.mixer.Sound(buffer=_synth(350, 750, 0.09, 0.35, "square")),
            "point": pygame.mixer.Sound(buffer=_ding()),
            "hit": pygame.mixer.Sound(buffer=_synth(280, 90, 0.25, 0.5, "triangle")),
            "fall": pygame.mixer.Sound(buffer=_synth(700, 140, 0.45, 0.4, "sine")),
        }
        return True
    except pygame.error:
        _sounds = {}
        return False
def play(name):
    """Play one of the pre-generated sounds by name; no-op if missing."""
    snd = _sounds.get(name)
    if snd is not None:
        try:
            snd.play()
        except pygame.error:
            pass