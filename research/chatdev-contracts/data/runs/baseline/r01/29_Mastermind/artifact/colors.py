'''
colors.py
ANSI color helpers for terminal output.
Provides ANSI escape-sequence constants, a mapping from playable color
symbols to terminal colors, and helpers to enable/detect color support
and wrap text in the appropriate color. Falls back to plain text on
terminals that do not support ANSI codes (or when output is redirected).
'''
import os
import sys
# ANSI escape sequences for styling terminal output.
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
# Map each playable color symbol to its ANSI color code.
COLOR_MAP = {
    "R": RED,
    "O": YELLOW,
    "Y": YELLOW,
    "G": GREEN,
    "B": BLUE,
    "P": MAGENTA,
    "W": WHITE,
    "K": CYAN,
}
# Module-level flag: True when ANSI colors may be emitted.
_COLORS_ENABLED = False
def enable_colors():
    """Enable ANSI colors when the terminal supports them; returns True if enabled."""
    global _COLORS_ENABLED
    if os.name == "nt":
        # Activates VT escape-sequence processing on Windows 10+ consoles.
        os.system("")
    _COLORS_ENABLED = sys.stdout.isatty()
    return _COLORS_ENABLED
def colorize(text, symbol):
    """Wrap text in the ANSI color for `symbol`; return plain text if colors are off."""
    if not _COLORS_ENABLED:
        return text
    color = COLOR_MAP.get(symbol.upper())
    return f"{color}{text}{RESET}" if color else text