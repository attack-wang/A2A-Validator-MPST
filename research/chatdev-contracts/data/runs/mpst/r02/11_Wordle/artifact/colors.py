'''
colors.py
Terminal color handling for the Wordle game.
Provides ANSI escape sequences and helper utilities to paint text with
foreground/background colours. Colour output can be disabled globally
(e.g. when the terminal does not support it, the NO_COLOR environment
variable is set, or the user passes --no-color).
'''
import os
import sys
# --- ANSI escape sequences -------------------------------------------------
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
FG_GREEN = "\033[92m"
FG_YELLOW = "\033[93m"
FG_GREY = "\033[90m"
FG_RED = "\033[91m"
FG_CYAN = "\033[96m"
FG_WHITE = "\033[97m"
BG_GREEN = "\033[48;5;108m"
BG_YELLOW = "\033[48;5;179m"
BG_GREY = "\033[48;5;240m"
BG_DEFAULT = "\033[49m"
_color_enabled = None
def detect_color_support() -> bool:
    """Return True if the current environment should render ANSI colours."""
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    if os.name != "posix":
        # The game targets Linux terminals; be conservative elsewhere.
        return sys.stdout.isatty() and os.environ.get("TERM") != "dumb"
    return sys.stdout.isatty() and os.environ.get("TERM", "") != "dumb"
def set_color_enabled(enabled: bool) -> None:
    """Explicitly enable/disable colour output (used by the --no-color flag)."""
    global _color_enabled
    _color_enabled = bool(enabled)
def color_enabled() -> bool:
    """Return whether colour output is currently enabled."""
    if _color_enabled is None:
        return detect_color_support()
    return _color_enabled
def paint(text: str, *codes: str) -> str:
    """Wrap *text* in the given ANSI codes if colours are enabled."""
    if not codes or not color_enabled():
        return text
    return "".join(codes) + text + RESET