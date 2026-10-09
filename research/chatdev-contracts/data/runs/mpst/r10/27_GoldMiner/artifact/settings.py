"""Central configuration constants for the Gold Miner game."""
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Gold Miner"
# Colors (R, G, B)
SKY_BLUE = (135, 206, 235)
DIRT_BROWN = (139, 90, 43)
DIRT_DARK = (110, 70, 30)
GROUND_GREEN = (34, 139, 34)
ROPE_COLOR = (90, 60, 30)
CLAW_COLOR = (70, 70, 70)
CLAW_DARK = (40, 40, 40)
GOLD_COLOR = (255, 200, 40)
GOLD_DARK = (200, 150, 20)
GOLD_SHINE = (255, 240, 180)
ROCK_COLOR = (130, 130, 130)
ROCK_DARK = (90, 90, 90)
DIAMOND_COLOR = (80, 220, 255)
DIAMOND_DARK = (30, 160, 200)
DIAMOND_SHINE = (230, 250, 255)
TNT_RED = (200, 40, 40)
TNT_DARK = (140, 20, 20)
TNT_TEXT = (255, 255, 255)
MYSTERY_COLOR = (160, 110, 60)
MYSTERY_DARK = (110, 75, 40)
TEXT_COLOR = (30, 30, 30)
HUD_BG = (20, 20, 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 40, 40)
GREEN = (40, 180, 60)
YELLOW = (255, 220, 60)
EXPLOSION_COLOR = (255, 140, 0)
EXPLOSION_COLOR2 = (255, 220, 0)
# Layout
PIVOT_X = SCREEN_WIDTH // 2
PIVOT_Y = 90
GROUND_Y = 150
MINE_TOP = GROUND_Y + 30
MINE_BOTTOM = SCREEN_HEIGHT - 30
MINE_MARGIN = 40
# Claw physics
ROPE_MIN_LENGTH = 60
ROPE_EXTEND_SPEED = 7.0
RETRACT_EMPTY_SPEED = 10.0
RETRACT_BASE_SPEED = 60.0  # divided by object weight when loaded
SWING_ANGLE_LIMIT = 75  # degrees from vertical
# TNT
TNT_EXPLOSION_RADIUS = 90
# Mystery bag possible values
MYSTERY_VALUES = [50, 100, 250, 600]
OBJECT_STATS = {
    "gold_small":  {"value": 50,  "weight": 1.0, "radius": 10},
    "gold_medium": {"value": 100, "weight": 2.0, "radius": 16},
    "gold_large":  {"value": 250, "weight": 3.5, "radius": 24},
    "rock_small":  {"value": 11,  "weight": 2.0, "radius": 12},
    "rock_large":  {"value": 20,  "weight": 4.0, "radius": 22},
    "diamond":     {"value": 600, "weight": 1.0, "radius": 12},
    "tnt":         {"value": 0,   "weight": 1.0, "radius": 14},
    "mystery_bag": {"value": 0,   "weight": 1.5, "radius": 14},
}
def level_config(number):
    """Ascending difficulty: tighter time, higher target, more hazards, faster swing."""
    return {
        "time_limit": max(30, 60 - (number - 1) * 5),
        "target_gold": 300 + (number - 1) * 250,
        "tnt_count": min(1 + (number - 1) // 2, 5),
        "rock_count": min(2 + number, 8),
        "gold_count": 6 + number // 2,
        "diamond_count": 1 if number >= 2 else 0,
        "mystery_count": 1,
        "swing_speed": 1.5 + 0.15 * (number - 1),
    }
MAX_LEVEL = 8  # victory after clearing this level