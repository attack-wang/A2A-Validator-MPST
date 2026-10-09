'''
colors.py
ANSI escape-code helpers for coloring terminal output.
'''
RESET = "\033[0m"
BOLD = "\033[1m"
FG_GREEN = "\033[92m"
FG_YELLOW = "\033[93m"
FG_GREY = "\033[90m"
FG_RED = "\033[91m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_GREY = "\033[100m"
# Semantic aliases used by feedback.py (background tiles read best).
GREEN = BG_GREEN
YELLOW = BG_YELLOW
GREY = BG_GREY
_color_enabled = True
def set_color_enabled(enabled):
    """Enable/disable ANSI coloring globally (e.g. for --no-color)."""
    global _color_enabled
    _color_enabled = bool(enabled)
def colorize(text, code):
    """Return text wrapped in the given ANSI code (or plain if disabled)."""
    if not _color_enabled:
        return text
    return f"{code}{text}{RESET}"
def tile(letter, feedback_color):
    """Return one colored tile, e.g. ' G ' with a green background."""
    return colorize(f" {letter.upper()} ", feedback_color)