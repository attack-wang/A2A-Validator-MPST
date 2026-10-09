'''
colors.py
Color palette definitions and terminal output helpers for the
Mastermind game. Maps color letters to human-readable names and ANSI
escape codes, detects Unicode support for the feedback pegs, and
provides helpers to colorize text and enable ANSI support on Windows
consoles.
'''
import os
import sys
# Letter -> color name (order defines the default palette).
COLOR_LETTERS = {
    "R": "Red",
    "G": "Green",
    "B": "Blue",
    "Y": "Yellow",
    "O": "Orange",
    "P": "Purple",
    "C": "Cyan",
    "M": "Magenta",
}
# Letter -> ANSI foreground escape code.
COLOR_ANSI = {
    "R": "\033[91m",   # bright red
    "G": "\033[92m",   # bright green
    "B": "\033[94m",   # bright blue
    "Y": "\033[93m",   # bright yellow
    "O": "\033[38;5;208m",  # orange (256-color)
    "P": "\033[95m",   # bright magenta (purple-ish)
    "C": "\033[96m",   # bright cyan
    "M": "\033[35m",   # magenta
}
ANSI_RESET = "\033[0m"
def enable_windows_ansi():
    """Enable ANSI escape-sequence processing on Windows consoles."""
    if os.name == "nt":
        os.system("")
def supports_unicode():
    """True when stdout can encode the Unicode feedback pegs."""
    try:
        "●○·".encode(sys.stdout.encoding or "utf-8")
        return True
    except (UnicodeEncodeError, LookupError):
        return False
def colorize(text, letter, enabled=True):
    """Wrap text in the ANSI color for `letter` when enabled."""
    if not enabled:
        return text
    return f"{COLOR_ANSI.get(letter, '')}{text}{ANSI_RESET}"