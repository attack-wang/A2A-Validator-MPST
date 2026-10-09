'''
config.py
Global configuration constants for the match-3 puzzle game.
'''
# Window / board layout
GRID_SIZE = 8
CELL_SIZE = 68
HUD_HEIGHT = 110
MARGIN = 12
WINDOW_WIDTH = GRID_SIZE * CELL_SIZE + MARGIN * 2
WINDOW_HEIGHT = HUD_HEIGHT + GRID_SIZE * CELL_SIZE + MARGIN * 2
BOARD_TOP = HUD_HEIGHT
BOARD_LEFT = MARGIN
FPS = 60
# Candies
NUM_CANDY_TYPES = 6
CANDY_COLORS = [...]
CANDY_NAMES = [...]
# Colors (UI)
...
# Gameplay
MAX_MOVES = 30
TARGET_SCORE = 5000
GAME_TIME_LIMIT = 300
# Scoring
SCORE_PER_CANDY = 60
FOUR_MATCH_BONUS = 120
FIVE_MATCH_BONUS = 300
COMBO_MULTIPLIER = 0.5  # extra multiplier per chain step? 
Actually let me define: score_for(matches, combo) = (base points) * combo where combo starts at 1. Or use COMBO_BONUS = 50 per chain level. Let me keep it simple: base = len(matches) * SCORE_PER_CANDY + bonuses for 4/5 runs; total = base * combo (combo >= 1).
# Animation timings
SWAP_DURATION = 0.18
CLEAR_DURATION = 0.28
FALL_ACCELERATION = 3800.0
MAX_FALL_SPEED = 1400.0
POPUP_LIFETIME = 0.9
# Fonts
FONT_NAME = None