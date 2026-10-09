'''Terminal color and rendering utilities for the Wordle game.'''
import os
import sys
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[1;2m"
FG_WHITE = "\033[97m"
FG_BLACK = "\033[30m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_GREY = "\033[100m"
FG_GREEN = "\033[92m"
FG_YELLOW = "\033[93m"
FG_GREY = "\033[90m"
FG_CYAN = "\033[96m"
FG_MAGENTA = "\033[95m"
# Feedback state constants
GREEN = "GREEN"
YELLOW = "YELLOW"
GREY = "GREY"
BG_FOR_STATE = {GREEN: BG_GREEN, YELLOW: BG_YELLOW, GREY: BG_GREY}
FG_FOR_STATE = {GREEN: FG_WHITE, YELLOW: FG_WHITE, GREY: FG_WHITE}
COLOR_ENABLED = True
def supports_color():
    """Return True when stdout is a TTY that supports ANSI colors and NO_COLOR is unset."""
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
def set_color_enabled(enabled):
    """Globally enable or disable ANSI color output (call once at startup)."""
    global COLOR_ENABLED
    COLOR_ENABLED = bool(enabled)
def colorize(text, color_code):
    """Wrap text in an ANSI color code; no-op when colors are disabled."""
    if not COLOR_ENABLED or not color_code:
        return text
    return f"{color_code}{text}{RESET}"
def render_guess_row(guess, feedback):
    """Render one guessed word as colored 3-character cells, e.g. ' C  R  A  N  E '."""
    cells = []
    for letter, state in zip(guess.upper(), feedback):
        bg = BG_FOR_STATE.get(state, "")
        fg = FG_FOR_STATE.get(state, "")
        cells.append(colorize(f" {letter} ", bg + fg))
    return " ".join(cells)
def render_keyboard(letter_states):
    """Render a QWERTY keyboard colored by each letter's best-known state."""
    rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
    lines = []
    for row in rows:
        cells = []
        for ch in row:
            state = letter_states.get(ch)
            if state:
                bg = BG_FOR_STATE[state]
                fg = FG_FOR_STATE[state]
                cells.append(colorize(f" {ch} ", bg + fg))
            else:
                cells.append(f" {ch} ")
        lines.append(" ".join(cells))
    return "\n".join(lines)