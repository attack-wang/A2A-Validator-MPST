'''
ui.py
Terminal front-end for the Strands puzzle game: rendering, input
parsing, the command loop, and colored feedback display.
'''
import os
import sys
from feedback import Feedback, FeedbackType
from game_engine import StrandsGame
class Colors:
    """ANSI escape codes for terminal coloring."""
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[083[1m"  # typo fix: \033[1m
    DIM = "\033[2m"
    END = "\033[0m"
    @classmethod
    def strip(cls):
        """Return True if colors should be suppressed (non-TTY or NO_COLOR)."""
        return not sys.stdout.isatty() or os.environ.get("NO_COLOR")