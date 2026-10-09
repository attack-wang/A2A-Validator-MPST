'''
ui.py - Display and rendering helpers for the Strands puzzle game.
Provides colorized console output (with NO_COLOR/FORCE_COLOR support and
non-TTY fallback), banner/menu/help screens, the numbered strand grid,
found-word tracker, merge feedback messages, hints, and completion stats.
'''
import os
import re
import sys
import shutil
class Color:
    """ANSI escape codes plus terminal-capability detection."""
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
    _ANSI_RE = re.compile(r"\033\[[0-9;]*m")
    _COLOR_ENABLED = None  # cached detection result
    @classmethod
    def enabled(cls):
        """Return True if the terminal is expected to render ANSI colors."""
        if cls._COLOR_ENABLED is None:
            forced = os.environ.get("FORCE_COLOR")
            no_color = os.environ.get("NO_COLOR")
            if no_color:
                cls._COLOR_ENABLED = False
            elif forced:
                cls._COLOR_ENABLED = True
            elif os.name == "nt":
                os.system("")  # enables ANSI VT processing on Windows 10+
                cls._COLOR_ENABLED = True
            else:
                cls._COLOR_ENABLED = (sys.stdout.isatty()
                                      and os.environ.get("TERM", "") != "dumb")
        return cls._COLOR_ENABLED
    @classmethod
    def strip_all(cls, text):
        """Remove every ANSI escape sequence from the given text."""
        return cls._ANSI_RE.sub("", text)
def supports_color():
    """Return True if the terminal is expected to render ANSI colors."""
    return Color.enabled()
def colorize(text, color=None):
    """Wrap text in ANSI color codes when the terminal supports them."""
    if color and Color.enabled():
        return f"{color}{text}{Color.RESET}"
    return text
def _safe_print(text=""):
    """Print text, degrading decorative Unicode to ASCII on old consoles."""
    try:
        print(text)
    except UnicodeEncodeError:
        for old, new in (("─", "-"), ("═", "="), ("★", "*"), ("●", "*"),
                         ("○", "-"), ("✓", "+"), ("✗", "x"), ("→", "->"),
                         ("“", '"'), ("”", '"')):
            text = text.replace(old, new)
        print(text)
def clear_screen():
    """Clear the terminal window; fall back to blank lines when unsupported."""
    try:
        if sys.stdout.isatty():
            os.system("cls" if os.name == "nt" else "clear")
        else:
            print("\n" * 2)
    except Exception:
        print("\n" * 2)
def print_divider(char="─", width=64):
    """Print a horizontal divider line."""
    _safe_print(colorize(char * width, Color.BLUE))
def print_banner():
    """Print the game title banner."""
    print_divider("═")
    _safe_print(colorize("S T R A N D S".center(64), Color.BOLD + Color.CYAN))
    _safe_print(colorize("Merge the strands to form the hidden words!".center(64), Color.CYAN))
    print_divider("═")