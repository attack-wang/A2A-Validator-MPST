# settings.py
'''
settings.py
Central configuration module for the Space Invaders game.
All tunable constants (screen size, speeds, colors, gameplay balance)
live here so behaviour can be adjusted from a single place.
This version uses only the Python standard library (tkinter), so the
game runs without any third-party dependencies such as pygame.
'''
def rgb_to_hex(rgb):
    """Convert an (r, g, b) tuple to a '#rrggbb' hex string for tkinter."""
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])
class Settings:
    """Holds every tunable constant used across the game."""
    # Window / general
    TITLE = "Space Invaders"
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FRAME_MS = 16          # ~60 FPS with tkinter's after() loop
    MAX_DT = 0.05
    BG_COLOR = "#080a19"   # (8, 10, 25)
    # Player ship
    SHIP_SPEED = 320.0
    SHIP_WIDTH = 44
    SHIP_HEIGHT = 26
    SHIP_COLOR = rgb_to_hex((0, 220, 255))
    SHIP_START_LIVES = 3
    SHIP_FIRE_COOLDOWN = 0.40
    MAX_PLAYER_BULLETS = 3
    INVINCIBILITY_TIME = 1.5
    SHIP_MARGIN = 10
    # Bullets
    BULLET_WIDTH = 4
    BULLET_HEIGHT = 16
    PLAYER_BULLET_SPEED = 520.0
    PLAYER_BULLET_COLOR = rgb_to_hex((0, 255, 120))
    ALIEN_BULLET_SPEED = 240.0
    ALIEN_BULLET_COLOR = rgb_to_hex((255, 80, 80))
    # Aliens / fleet
    ALIEN_ROWS = 4
    ALIEN_COLS = 8
    ALIEN_WIDTH = 36
    ALIEN_HEIGHT = 26
    ALIEN_X_SPACING = 18
    ALIEN_Y_SPACING = 16
    FLEET_TOP_OFFSET = 80
    FLEET_SIDE_MARGIN = 20
    ALIEN_BASE_SPEED = 45.0
    ALIEN_WAVE_SPEED_BONUS = 20.0
    ALIEN_RUSH_FACTOR = 2.2
    ALIEN_DESCENT_STEP = 18
    ALIEN_POINTS = [30, 25, 20, 15, 10]
    ALIEN_COLORS = [rgb_to_hex(c) for c in [
        (170, 120, 255),
        (80, 200, 255),
        (120, 255, 120),
        (255, 200, 60),
    ]]
    # Alien firing
    ALIEN_FIRE_MIN = 0.6
    ALIEN_FIRE_MAX = 1.8
    ALIEN_FIRE_WAVE_SCALE = 0.85
    # Waves
    MAX_WAVES = 3
    WAVE_CLEAR_BONUS = 100
    WAVE_MESSAGE_TIME = 2.0
    # UI
    HUD_COLOR = rgb_to_hex((230, 230, 230))
    ACCENT_COLOR = rgb_to_hex((0, 220, 255))
    DANGER_COLOR = rgb_to_hex((255, 90, 90))
    SUCCESS_COLOR = rgb_to_hex((120, 255, 120))
    FONT_FAMILY = "Consolas"