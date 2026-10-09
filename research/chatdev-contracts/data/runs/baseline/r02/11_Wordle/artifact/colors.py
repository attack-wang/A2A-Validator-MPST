'''
colors.py
Defines ANSI escape sequences used to color terminal output and provides
a small helper to wrap text with a given color. Works on any ANSI-capable
Linux terminal.
'''
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[1;30;42m"   # bold black text on green background
YELLOW = "\033[1;30;43m"  # bold black text on yellow background
GREY = "\033[1;37;100m"   # bold white text on dark grey background
def colorize(text, color):
    """Wrap text with the given ANSI color code and reset afterwards."""
    return f"{color}{text}{RESET}"