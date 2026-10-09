'''
settings.py
Global configuration constants for the Gold Miner game.
Contains screen dimensions, colors, gameplay tuning values and
per-object statistics tables used across all other modules.
'''
# ---------------------------------------------------------------------------
# Screen / window
# ---------------------------------------------------------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WINDOW_TITLE = "Gold Miner"
# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
SUN_YELLOW = (255, 230, 90)
DIRT_BROWN = (133, 87, 45)
DIRT_DARK = (100, 64, 32)
DIRT_LIGHT = (160, 110, 60)
GOLD_YELLOW = (255, 200, 40)
GOLD_DARK = (180, 130, 20)
GRAY = (128, 128, 128)
GRAY_DARK = (90, 90, 90)
RED = (220, 60, 60)
CYAN = (60, 200, 220)
PURPLE = (150, 60, 200)
GREEN = (60, 180, 80)
ROPE_COLOR = (70, 50, 30)
CLAW_COLOR = (60, 60, 70)
HUD_BG = (25, 25, 35)
HUD_TEXT = (255, 255, 255)
TIME_WARN = (255, 80, 80)
# ---------------------------------------------------------------------------
# Mining field layout
# ---------------------------------------------------------------------------
GROUND_Y = 140          # y coordinate where the dirt field begins
PIVOT_X = SCREEN_WIDTH // 2
PIVOT_Y = 90            # pulley the claw hangs from (inside the sky band)
# ---------------------------------------------------------------------------
# Claw physics (angles measured in degrees; 90 = straight down)
# ---------------------------------------------------------------------------
CLAW_MIN_LENGTH = 60
CLAW_MAX_LENGTH = 520
CLAW_MIN_ANGLE = 25.0
CLAW_MAX_ANGLE = 155.0
CLAW_EXTEND_SPEED = 9.0        # pixels per frame while shooting out
CLAW_RETRACT_EMPTY_SPEED = 7.0 # pixels per frame when reeling nothing in
CLAW_GRAB_RADIUS = 10          # extra reach around the claw tip
# ---------------------------------------------------------------------------
# Collectible statistics: kind -> radius / value / weight
# weight >= 1.0 always: retract speed = CLAW_RETRACT_EMPTY_SPEED / weight,
# so heavier objects always take LONGER to reel in (never shorter).
# ---------------------------------------------------------------------------
OBJECT_STATS = {
    "gold_small":  {"radius": 12, "value":  50,  "weight": 1.0},
    "gold_medium": {"radius": 20, "value": 120,  "weight": 1.8},
    "gold_large":  {"radius": 30, "value": 250,  "weight": 3.0},
    "rock":        {"radius": 24, "value":  20,  "weight": 2.8},
    "diamond":     {"radius": 12, "value": 600,  "weight": 1.2},
    "skull":       {"radius": 16, "value": -80,  "weight": 1.5},
}