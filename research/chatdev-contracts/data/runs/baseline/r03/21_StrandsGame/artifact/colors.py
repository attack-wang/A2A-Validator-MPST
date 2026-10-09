'''
colors.py
ANSI terminal color and style constants used by the Strands puzzle game.
Each constant is a plain string escape sequence. Use RESET after any
colored output to return the terminal to its default style.
'''
# --- Style modifiers ---
RESET = "\033[0m"    # Reset all attributes
BOLD = "\033[1m"     # Bold / increased intensity
DIM = "\033[2m"      # Dimmed intensity (used for consumed strands)
# --- Foreground colors ---
FG_RED = "\033[31m"     # Invalid merge feedback
FG_GREEN = "\033[32m"   # Valid merge feedback
FG_YELLOW = "\033[33m"  # Warnings / hints
FG_BLUE = "\033[34m"    # Informational messages
FG_MAGENTA = "\033[35m" # Titles / banners
FG_CYAN = "\033[36m"    # Board rendering
FG_WHITE = "\033[37m"   # Default text
# --- Background colors ---
BG_BLUE = "\033[44m"    # Header banner background
BG_GREEN = "\033[42m"   # Completion banner background
BG_MAGENTA = "\033[45m" # Title background
def paint(text, *styles):
    """Wrap `text` in the given ANSI styles followed by RESET."""
    return "".join(styles) + str(text) + RESET
def supports_color():
    """Return True if the terminal likely supports ANSI escape codes."""
    import os
    import sys
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("TERM") == "dumb":
        return False
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()