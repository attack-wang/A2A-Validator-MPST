"""Global configuration constants for the Space Invaders game."""
# Screen / window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
FRAME_MS = max(1, 1000 // FPS)
WINDOW_TITLE = "Space Invaders"
# Colors (hex strings usable by Tk)
COLOR_BACKGROUND = "#080a18"
COLOR_WHITE = "#ebebeb"
COLOR_GREEN = "#50dc64"
COLOR_CYAN = "#5ac8e6"
COLOR_RED = "#eb5555"
COLOR_YELLOW = "#f5d246"
COLOR_PURPLE = "#be78f0"
COLOR_ORANGE = "#f5963c"
COLOR_GREY = "#9696a0"
# Ship (speeds are pixels per second, timers in seconds)
SHIP_SPEED = 300.0
SHIP_COOLDOWN = 0.35
SHIP_MAX_BULLETS = 3
SHIP_START_LIVES = 3
SHIP_INVINCIBILITY = 1.5
# Player bullets
PLAYER_BULLET_SPEED = 480.0
PLAYER_BULLET_WIDTH = 3
PLAYER_BULLET_HEIGHT = 14
# Alien bombs
ALIEN_BOMB_SPEED = 210.0
ALIEN_BOMB_WIDTH = 3
ALIEN_BOMB_HEIGHT = 12
ALIEN_BOMB_CHANCE = 0.7      # expected bombs per second
ALIEN_BOMB_COOLDOWN = 0.45   # minimum seconds between bombs
# Alien fleet
ALIEN_ROWS = 5
ALIEN_COLS = 8
ALIEN_BASE_SPEED = 36.0
ALIEN_MAX_SPEED = 190.0
ALIEN_DROP_DISTANCE = 22
ALIEN_HORIZONTAL_PADDING = 60
ALIEN_TOP_OFFSET = 90
ALIEN_SPACING_X = 56
ALIEN_SPACING_Y = 48
ALIEN_POINTS_TOP = 30
ALIEN_POINTS_MIDDLE = 20
ALIEN_POINTS_BOTTOM = 10
ALIEN_BOTTOM_LIMIT = 90
# HUD / fonts (pixel sizes for tkfont)
FONT_SMALL = 12
FONT_MEDIUM = 16
FONT_LARGE = 30