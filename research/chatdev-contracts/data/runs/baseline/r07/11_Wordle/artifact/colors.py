'''
colors.py
ANSI escape-code helpers for coloring terminal output.
Provides named color codes (green, yellow, grey, red, cyan, bold) and a
small utility, colorize(), that wraps text with an optional bold modifier.
Colors can be disabled globally via disable_colors() (used when the
terminal does not support ANSI codes or the user passes --no-color).
'''
import os
import sys
# ANSI escape sequences
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
GREY = "\033[90m"
RED = "\033[91m"
CYAN = "\033[96m"
_colors_enabled = True
def disable_colors():
    """Globally disable ANSI coloring (all colorize calls become plain text)."""
    global _colors_enabled
    _colors_enabled = False
def colors_enabled():
    return _colors_enabled
def detect_color_support():
    """Auto-detect whether stdout can display ANSI colors."""
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("TERM") == "dumb":
        return False
    return sys.stdout.isatty()
def colorize(text, color, bold=False):
    """Wrap text in the given ANSI color (plus optional bold)."""
    if not _colors_enabled:
        return text
    prefix = BOLD if bold else ""
    return f"{prefix}{color}{text}{RESET}"