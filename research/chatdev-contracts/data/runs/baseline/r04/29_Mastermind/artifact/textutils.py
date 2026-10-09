'''
textutils.py
ANSI-aware text helpers shared by the rendering code.
Terminal color escape sequences are invisible on screen yet count as
characters inside Python strings, so plain str.ljust()/format() padding
would misalign any column that contains colored text. The helpers here
measure the *visible* width (escape codes stripped) and pad accordingly.
'''
import re
# Matches ANSI SGR escape sequences such as "\033[0m" or "\033[38;5;208m".
ANSI_PATTERN = re.compile(r"\033\[[0-9;]*m")
def visible_width(text):
    """Number of characters `text` occupies once ANSI codes are removed."""
    return len(ANSI_PATTERN.sub("", text))
def pad(text, width):
    """Right-pad `text` with spaces up to `width` visible columns."""
    return text + " " * max(0, width - visible_width(text))