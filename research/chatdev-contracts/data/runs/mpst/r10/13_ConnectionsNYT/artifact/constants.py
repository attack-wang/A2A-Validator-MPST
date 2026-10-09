'''
constants.py
Central configuration for the ChatDev Connections puzzle game.
Defines the difficulty tiers with their signature colors (yellow, green,
blue, purple), game rule constants (grid size, maximum mistakes), and
UI styling values shared across the application.
'''
# --- Game rules -----------------------------------------------------------
GRID_SIZE = 4          # The word grid is GRID_SIZE x GRID_SIZE (16 words)
WORDS_PER_GROUP = 4    # Each hidden category contains exactly four words
MAX_MISTAKES = 4       # The game is lost after this many incorrect guesses
# --- Difficulty tiers -----------------------------------------------------
# Ordered from easiest (yellow) to hardest (purple).
DIFFICULTY_ORDER = ("yellow", "green", "blue", "purple")
DIFFICULTY_COLORS = {
    "yellow": "#F9DF6A",   # Straightforward
    "green":  "#A0C35A",   # A little trickier
    "blue":   "#B0C4EF",   # Tricky
    "purple": "#BA81C5",   # Devious / wordplay
}
DIFFICULTY_LABELS = {
    "yellow": "Straightforward",
    "green":  "A little tricky",
    "blue":   "Tricky",
    "purple": "Devious",
}
# --- UI styling -----------------------------------------------------------
WINDOW_TITLE = "ChatDev Connections"
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 820
BG_COLOR = "#FFFFFF"
TILE_BG = "#EFEFE7"
TILE_BG_SELECTED = "#5A594E"
TILE_FG = "#5A594E"
TILE_FG_SELECTED = "#FFFFFF"
TILE_FONT = ("Helvetica", 12, "bold")
ACCENT_COLOR = "#5A594E"
BANNER_TEXT_COLOR = "#333333"
...