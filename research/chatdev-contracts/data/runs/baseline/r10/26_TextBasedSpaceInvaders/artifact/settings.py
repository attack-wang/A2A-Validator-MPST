'''
settings.py
Central configuration for the Space Invaders game. All tunable constants
(screen size, colors, speeds, scoring, difficulty) live here so the game
can be balanced without touching the game logic.
'''
# --- Screen / timing -------------------------------------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Space Invaders"
# --- Colors ----------------------------------------------------------------
BLACK = (10, 10, 20)
WHITE = (240, 240, 240)
GREEN = (80, 220, 100)
RED = (235, 80, 80)
CYAN = (80, 200, 255)
YELLOW = (250, 210, 70)
PURPLE = (190, 120, 255)
GREY = (120, 120, 130)
# --- Player ----------------------------------------------------------------
PLAYER_WIDTH = 44
PLAYER_HEIGHT = 26
PLAYER_SPEED = 6.0            # pixels per frame
PLAYER_COOLDOWN_MS = 400      # minimum ms between shots
PLAYER_START_LIVES = 3
PLAYER_RESPAWN_INVULN_MS = 1500  # invulnerability after being hit
PLAYER_BOTTOM_OFFSET = 30
# --- Bullets ---------------------------------------------------------------
BULLET_WIDTH = 4
BULLET_HEIGHT = 16
PLAYER_BULLET_SPEED = 9.0     # pixels per frame (upwards)
ALIEN_BULLET_SPEED = 4.5      # pixels per frame (downwards)
# --- Alien formation -------------------------------------------------------
ALIEN_ROWS = 5
ALIEN_COLS = 8
ALIEN_WIDTH = 38
ALIEN_HEIGHT = 26
ALIEN_H_SPACING = 16
ALIEN_V_SPACING = 16
ALIEN_TOP_MARGIN = 90
ALIEN_SIDE_MARGIN = 40
ALIEN_BASE_SPEED = 1.0        # pixels per frame at full strength
ALIEN_SPEED_PER_KILL = 0.06   # formation speeds up with every kill
ALIEN_DESCENT = 18            # pixels dropped when formation hits an edge
ALIEN_FIRE_CHANCE = 0.035     # per-frame chance that a column fires
ALIEN_ANIM_MS = 400           # animation toggle interval
# --- Alien colors ----------------------------------------------------------
# One color per row; cycled if ALIEN_ROWS ever exceeds the list length.
ALIEN_ROW_COLORS = [PURPLE, GREEN, CYAN, YELLOW, RED]
# --- Scoring ---------------------------------------------------------------
# Points awarded per alien, keyed by row index (0 = top row).
SCORE_PER_ROW = {0: 30, 1: 20, 2: 20, 3: 10, 4: 10}
DEFAULT_ALIEN_SCORE = 10
# --- Game flow -------------------------------------------------------------
GAME_OVER_TITLE = "GAME OVER"
VICTORY_TITLE = "VICTORY!"
RESTART_HINT = "Press R to play again  -  ESC to quit"