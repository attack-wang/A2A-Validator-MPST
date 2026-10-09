'''
colors.py
Terminal color helpers for the Mastermind game.
Provides best-effort ANSI color activation, a bold() text wrapper,
per-color peg coloring, the active palette slice, and the letter
shortcuts used when typing guesses. Falls back gracefully to plain
text when the terminal does not support ANSI escape codes.
'''
import os
import sys
# ANSI escape sequences for the supported palette colors.
_ANSI = {
    "red": "\033[91m",
    "green": "\033[92m",
    "blue": "\033[94m",
    "yellow": "\033[93m",
    "orange": "\033[38;5;208m",
    "purple": "\033[95m",
    "cyan": "\033[96m",
    "magenta": "\033[35m",
    "white": "\033[97m",
}
_RESET = "\033[0m"
_BOLD = "\033[1m"
# First letters of the ANSI palette names are unique (R, G, B, Y, O, P, C, M, W),
# so single-letter shortcuts can be resolved back to full color names.
_SHORTCUT_TO_NAME = {name[0]: name for name in _ANSI}
_colors_enabled = None  # set by enable_colors()
def enable_colors():
    """Best-effort activation of ANSI colors on the current terminal."""
    global _colors_enabled
    if os.name == "nt":
        os.system("")  # Enables ANSI escape processing on modern Windows terminals
    _colors_enabled = sys.stdout.isatty()
    return _colors_enabled
def _wrap(text, code):
    """Wrap text in an ANSI escape code when colors are enabled."""
    if _colors_enabled:
        return f"{code}{text}{_RESET}"
    return text
def bold(text):
    """Return text wrapped in ANSI bold when colors are enabled."""
    return _wrap(text, _BOLD)
def peg(text):
    """Colorize a color name or its single-letter shortcut for display."""
    key = text.strip().lower()
    name = key if key in _ANSI else _SHORTCUT_TO_NAME.get(key)
    if name is None:
        return text
    return _wrap(text, _ANSI[name])
def active_colors(palette, palette_size):
    """Return the first `palette_size` colors of the given palette."""
    if palette_size > len(palette):
        raise ValueError(
            f"palette_size {palette_size} exceeds palette length {len(palette)}."
        )
    return list(palette[:palette_size])
def letter_for(color_name):
    """Return the unique single-letter shortcut for a color name."""
    return color_name[0].lower()
def build_letter_map(color_names):
    """Map each color's unique first letter (lowercased) to the color name."""
    mapping = {}
    for name in color_names:
        letter = name[0].lower()
        if letter in mapping:
            raise ValueError(
                f"Duplicate letter shortcut '{letter}' for colors "
                f"'{mapping[letter]}' and '{name}'."
            )
        mapping[letter] = name
    return mapping