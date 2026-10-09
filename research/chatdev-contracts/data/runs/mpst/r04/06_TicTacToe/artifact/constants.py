'''
constants.py
Defines shared configuration constants for the tic-tac-toe application,
including board dimensions, player symbols, color palette, and fonts used
by the graphical interface.
'''
# --- Board configuration -------------------------------------------------
BOARD_SIZE = 3          # Standard 3x3 tic-tac-toe grid
EMPTY = " "             # Symbol representing an unplayed cell
# --- Player configuration ------------------------------------------------
PLAYER_X = "X"
PLAYER_O = "O"
PLAYERS = (PLAYER_X, PLAYER_O)
DRAW_KEY = "Draws"      # Key used for tallying drawn games
# --- Window configuration ------------------------------------------------
WINDOW_TITLE = "Tic-Tac-Toe"
BG_COLOR = "#1B2430"        # Main window background
TEXT_COLOR = "#EAEFF7"      # Primary text color
MUTED_TEXT_COLOR = "#8FA3BF"  # Secondary text color
# --- Cell appearance -----------------------------------------------------
CELL_COLOR = "#2E3B4E"        # Default cell background
CELL_HOVER_COLOR = "#3E5068"  # Cell background while hovered (empty cells)
CELL_TEXT_COLOR = "#EAEFF7"   # Fallback text color for empty cells
X_COLOR = "#FF6B6B"           # Color used for player X marks
O_COLOR = "#4ECDC4"           # Color used for player O marks
WIN_HIGHLIGHT_COLOR = "#FFD166"  # Background for winning-line cells
WIN_TEXT_COLOR = "#1B2430"    # Text color on highlighted winning cells
# --- Fonts ---------------------------------------------------------------
TITLE_FONT = ("Helvetica", 22, "bold")
STATUS_FONT = ("Helvetica", 14, "bold")
SCORE_FONT = ("Helvetica", 12)
CELL_FONT = ("Helvetica", 28, "bold")
BUTTON_FONT = ("Helvetica", 12, "bold")
# --- Control buttons -----------------------------------------------------
ACCENT_COLOR = "#4ECDC4"        # Reset-button background
ACCENT_HOVER_COLOR = "#6FDAD1"  # Reset-button hover background
ACCENT_TEXT_COLOR = "#10231F"   # Reset-button text color