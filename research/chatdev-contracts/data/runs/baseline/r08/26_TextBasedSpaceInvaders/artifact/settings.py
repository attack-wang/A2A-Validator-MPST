'''
settings.py
Central configuration module for the Space Invaders game.
All tunable constants (screen size, speeds, colors, gameplay balance)
live here so behaviour can be adjusted from a single place.
'''
class Settings:
    """Holds every tunable constant used across the game."""
    # ------------------------------------------------------------------
    # Window / general
    # ------------------------------------------------------------------
    TITLE = "Space Invaders"
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60
    MAX_DT = 0.05          # clamp for delta time so pauses don't break physics
    BG_COLOR = (8, 10, 25)
    # ------------------------------------------------------------------
    # Player ship
    # ------------------------------------------------------------------
    SHIP_SPEED = 320.0            # pixels per second
    SHIP_WIDTH = 44
    SHIP_HEIGHT = 26
    SHIP_COLOR = (0, 220, 255)
    SHIP_START_LIVES = 3
    SHIP_FIRE_COOLDOWN = 0.40     # seconds between shots
    MAX_PLAYER_BULLETS = 3        # bullets allowed on screen at once
    INVINCIBILITY_TIME = 1.5      # seconds of safety after being hit
    SHIP_MARGIN = 10              # distance kept from screen edges
    # ------------------------------------------------------------------
    # Bullets
    # ------------------------------------------------------------------
    BULLET_WIDTH = 4
    BULLET_HEIGHT = 16
    PLAYER_BULLET_SPEED = 520.0
    PLAYER_BULLET_COLOR = (0, 255, 120)
    ALIEN_BULLET_SPEED = 240.0
    ALIEN_BULLET_COLOR = (255, 80, 80)
    # ------------------------------------------------------------------
    # Aliens / fleet
    # ------------------------------------------------------------------
    ALIEN_ROWS = 4
    ALIEN_COLS = 8
    ALIEN_WIDTH = 36
    ALIEN_HEIGHT = 26
    ALIEN_X_SPACING = 18          # horizontal gap between aliens
    ALIEN_Y_SPACING = 16          # vertical gap between aliens
    FLEET_TOP_OFFSET = 80         # y position of the first alien row
    FLEET_SIDE_MARGIN = 20        # fleet may not pass this close to edges
    ALIEN_BASE_SPEED = 45.0       # horizontal speed of the fleet (wave 1)
    ALIEN_WAVE_SPEED_BONUS = 20.0 # extra fleet speed per wave
    ALIEN_RUSH_FACTOR = 2.2       # speed multiplier when few aliens remain
    ALIEN_DESCENT_STEP = 18       # pixels dropped each time fleet reverses
    # Points awarded per row (index 0 = top row). Extra rows reuse last value.
    ALIEN_POINTS = [30, 25, 20, 15, 10]
    ALIEN_COLORS = [
        (170, 120, 255),   # top row - purple
        (80, 200, 255),    # second row - blue
        (120, 255, 120),   # third row - green
        (255, 200, 60),    # bottom row - yellow
    ]
    # Alien firing
    ALIEN_FIRE_MIN = 0.6          # fastest possible gap between alien shots
    ALIEN_FIRE_MAX = 1.8          # slowest possible gap (wave 1)
    ALIEN_FIRE_WAVE_SCALE = 0.85  # fire gaps shrink by this factor per wave
    # ------------------------------------------------------------------
    # Waves / progression
    # ------------------------------------------------------------------
    MAX_WAVES = 3
    WAVE_CLEAR_BONUS = 100        # bonus points multiplied by wave number
    WAVE_MESSAGE_TIME = 2.0       # seconds the "wave cleared" banner lasts
    # ------------------------------------------------------------------
    # UI / text
    # ------------------------------------------------------------------
    HUD_COLOR = (230, 230, 230)
    ACCENT_COLOR = (0, 220, 255)
    DANGER_COLOR = (255, 90, 90)
    SUCCESS_COLOR = (120, 255, 120)