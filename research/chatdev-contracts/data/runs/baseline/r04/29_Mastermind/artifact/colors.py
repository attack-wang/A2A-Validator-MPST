'''
colors.py
Color palette and terminal helpers for the Mastermind game.
Defines the Color descriptors (name, keyboard letter, ANSI escape code) and
the Palette used to render colored pegs. Also contains setup_terminal(),
which enables ANSI escape sequences on Windows terminals so the game looks
correct on every major platform without third-party dependencies.
'''
import os
import sys
RESET = "\033[0m"
DIM = "\033[2m"
BOLD = "\033[1m"
class Color:
    """A single peg color: display name, keyboard letter and ANSI code."""
    def __init__(self, name, letter, ansi):
        self.name = name
        self.letter = letter
        self.ansi = ansi
    def peg(self):
        """Return the peg glyph (filled circle) tinted with this color."""
        return f"{self.ansi}●{RESET}"
class Palette:
    """Ordered collection of colors available in a game."""
    def __init__(self, colors):
        self.colors = list(colors)
    def __len__(self):
        return len(self.colors)
    def __iter__(self):
        return iter(self.colors)
    def size(self):
        return len(self.colors)
    def get(self, index):
        """Return the Color at a 0-based index (validated)."""
        if not 0 <= index < len(self.colors):
            raise ValueError(
                f"color index {index + 1} is out of range 1-{len(self.colors)}"
            )
        return self.colors[index]
    def index_by_token(self, token):
        """Map a user token (digit, letter or color name) to a color index.
        Returns the 0-based index, or None when the token is not recognized.
        """
        token = token.strip().lower()
        if not token:
            return None
        if token.isdigit():
            number = int(token)
            if 1 <= number <= len(self.colors):
                return number - 1
            return None
        if len(token) == 1:
            for index, color in enumerate(self.colors):
                if color.letter.lower() == token:
                    return index
            return None
        for index, color in enumerate(self.colors):
            if color.name.lower() == token:
                return index
        return None
    def legend(self):
        """Return a one-line legend like '1=Red(R) 2=Green(G) ...'."""
        parts = []
        for index, color in enumerate(self.colors):
            parts.append(
                f"{color.ansi}{index + 1}={color.name}({color.letter}){RESET}"
            )
        return "  ".join(parts)
def build_palette(palette_size):
    """Build the standard palette truncated to `palette_size` colors."""
    base = [
        Color("Red", "R", "\033[91m"),
        Color("Green", "G", "\033[92m"),
        Color("Blue", "B", "\033[94m"),
        Color("Yellow", "Y", "\033[93m"),
        Color("Magenta", "M", "\033[95m"),
        Color("Cyan", "C", "\033[96m"),
        Color("Orange", "O", "\033[38;5;208m"),
        Color("White", "W", "\033[97m"),
    ]
    if palette_size < 1 or palette_size > len(base):
        raise ValueError(f"palette size must be between 1 and {len(base)}")
    return Palette(base[:palette_size])
def setup_terminal():
    """Prepare the terminal for ANSI colors and Unicode pegs."""
    if os.name == "nt":
        # Sending an empty string makes Windows 10+ consoles enable VT processing.
        os.system("")
    for stream in (sys.stdout, sys.stderr):
        try:
            if getattr(stream, "encoding", "").lower().replace("-", "") not in ("utf8", ""):
                stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass