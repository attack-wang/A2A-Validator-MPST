'''
colors.py
ANSI color constants and helpers for terminal rendering.
'''
import sys
# ANSI escape codes
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[38;5;10m\033[48;5;28m"  # or simpler
YELLOW = "\033[38;5;11m\033[48;5;178m"
GREY = "\033[38;5;15m\033[48;5;240m"
WHITE = "\033[0m"
RED = "\033[91m"
CYAN = "\033[96m"
def _supports_color():
    ...
def paint_feedback(letter, feedback, enabled=True):
    ...