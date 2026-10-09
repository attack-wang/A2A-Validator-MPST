'''
ui.py
Terminal UI helpers: ANSI coloring with graceful fallback, peg rendering,
palette display, and screen management.
'''
import os
import sys
from config import COLOR_ANSI, EXACT_PEG, PARTIAL_PEG, EMPTY_PEG
def _supports_color():
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    if sys.platform == "win32":
        os.system("")  # enables VT processing on Windows 10+
        return True
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
USE_COLOR = _supports_color()
def colorize(text, color_code):
    if USE_COLOR:
        return f"\033[{color_code}m{text}\033[0m"
    return str(text)
def paint(text, color_code):
    """Wrap text in an ANSI color sequence when the terminal supports it."""
    return colorize(text, color_code)
def paint_color_letter(letter):
    """Tint a palette letter with its own color from config.COLOR_ANSI."""
    return paint(letter, COLOR_ANSI.get(letter, "37"))
def palette_line(palette):
    """Render the available colors as one tinted line."""
    return "  ".join(paint_color_letter(letter) for letter in palette)
def clear_screen():
    """Return an ANSI clear-screen sequence (empty string if colors off)."""
    return "\033[2J\033[H" if USE_COLOR else ""
def banner():
    """Return the game title banner."""
    return paint("==== MASTERMIND ====", "95")
def render_pegs(feedback, code_length):
    pegs = ([paint(EXACT_PEG, "92")] * feedback.exact_matches +
            [paint(PARTIAL_PEG, "93")] * feedback.partial_matches +
            [EMPTY_PEG] * (code_length - feedback.exact_matches - feedback.partial_matches))
    return " ".join(pegs)