'''
ANSI color/style constants and helpers for terminal output.
'''
import os
import sys
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN_BG = "\033[1;37;42m"
YELLOW_BG = "\033[1;37;43m"
GREY_BG = "\033[1;37;100m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
GREY = "\033[90m"
GREEN = "\033[32m"
RED = "\033[31m"
def supports_color():
    if os.environ.get("NO_COLOR"):
        return False
    if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
        return False
    term = os.environ.get("TERM", "")
    if term == "dumb":
        return False
    return True
def colorize(text, style):
    if not style:
        return text
    return f"{style}{text}{RESET}"