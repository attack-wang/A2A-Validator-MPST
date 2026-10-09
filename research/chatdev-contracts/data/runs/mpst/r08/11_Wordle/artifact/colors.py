'''
colors.py
ANSI color utilities for the terminal Wordle game.
Defines the feedback colors (green / yellow / grey) and a colorize()
helper that wraps text in ANSI escape codes, degrading gracefully to
plain text when the terminal does not support colors.
'''
import os
import sys
# ANSI escape codes for terminal colors
GREEN = "\033[92m"    # correct letter, correct position
YELLOW = "\033[93m"   # correct letter, wrong position
GREY = "\033[90m"     # letter not in the word
RESET = "\033[0m"     # reset to default terminal style
def _supports_color():
    """Return True if stdout is a terminal that supports ANSI colors."""
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("TERM", "").lower() == "dumb":
        return False
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
_COLOR_ENABLED = _supports_color()
def colorize(text, color):
    """Wrap text in the given ANSI color, or return it unchanged when
    the terminal does not support colors."""
    if not _COLOR_ENABLED:
        return text
    return "{}{}{}".format(color, text, RESET)