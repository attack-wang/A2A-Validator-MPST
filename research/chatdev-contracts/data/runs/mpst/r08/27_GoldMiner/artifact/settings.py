'''Global settings and constants for the Gold Miner game.'''
# Screen
WIDTH = 800
HEIGHT = 600
FPS = 60
# Colors (R, G, B)
SKY_BLUE = (135, 206, 235)
DIRT_BROWN = (139, 90, 43)
DIRT_DARK = (101, 67, 33)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 200, 40)
GOLD_DARK = (200, 150, 20)
GRAY = (128, 128, 128)
GRAY_DARK = (90, 90, 90)
CYAN = (0, 220, 220)
RED = (220, 40, 40)
BONE_WHITE = (240, 235, 215)
GREEN = (60, 180, 75)
ORANGE = (255, 140, 0)
HUD_BG = (40, 40, 60)
# Layout
HUD_HEIGHT = 70
SURFACE_Y = HUD_HEIGHT
MINE_TOP = SURFACE_Y + 30
MINE_LEFT = 40
MINE_RIGHT = WIDTH - 40
MINE_BOTTOM = HEIGHT - 30
PIVOT = (WIDTH // 2, SURFACE_Y + 6)
# Claw
CLAW_MIN_LENGTH = 24
CLAW_SWING_SPEED = 70.0
CLAW_EXTEND_SPEED = 420.0
CLAW_RETRACT_EMPTY_SPEED = 620.0
CLAW_RETRACT_BASE_SPEED = 330.0
CLAW_MAX_ANGLE = 78.0
CLAW_TIP_RADIUS = 14
CLAW_MAX_LENGTH = MINE_BOTTOM - PIVOT[1] + 40
# Object kinds: value, weight (reel time factor), radius
OBJECT_STATS = {
    'small_gold':  {'value': 60,  'weight': 1.0, 'radius': 12},
    'medium_gold': {'value': 160, 'weight': 2.0, 'radius': 18},
    'large_gold':  {'value': 500, 'weight': 4.0, 'radius': 26},
    'diamond':     {'value': 620, 'weight': 1.2, 'radius': 13},
    'rock_small':  {'value': 20,  'weight': 3.0, 'radius': 16},
    'rock_big':    {'value': 35,  'weight': 5.5, 'radius': 25},
    'bone':        {'value': 15,  'weight': 2.2, 'radius': 14},
    'tnt':         {'value': 0,   'weight': 1.0, 'radius': 14},
    'mystery':     {'value': 0,   'weight': 2.0, 'radius': 15},
}
TNT_BLAST_RADIUS = 90
GOLD_KINDS = ('small_gold', 'medium_gold', 'large_gold', 'diamond', 'mystery')
def get_level_config(level):
    """Return difficulty parameters for the given level (1-based).
    Difficulty ascends: tighter time limits, faster claw swing, more
    worthless objects and TNT, and a higher gold target per level.
    """
    level = max(1, int(level))
    time_limit = max(30.0, 65.0 - 5.0 * (level - 1))
    swing_speed = CLAW_SWING_SPEED + 10.0 * (level - 1)
    extend_speed = CLAW_EXTEND_SPEED + 20.0 * (level - 1)
    counts = {
        'small_gold':  max(3, 6 - (level - 1) // 2),
        'medium_gold': max(2, 4 - (level - 1) // 3),
        'large_gold':  min(4, 1 + (level - 1) // 2),
        'diamond':     min(3, 1 + (level - 1) // 3),
        'rock_small':  min(6, 1 + level),
        'rock_big':    min(4, level // 2),
        'bone':        min(4, 1 + level // 2),
        'tnt':         min(4, level // 2),
        'mystery':     1 + (level - 1) // 2,
    }
    potential = (counts['small_gold'] * 60 + counts['medium_gold'] * 160 +
                 counts['large_gold'] * 500 + counts['diamond'] * 620 +
                 counts['mystery'] * 200)
    target = min(350 + 150 * (level - 1), int(potential * 0.6))
    return {
        'level': level,
        'target': target,
        'time_limit': time_limit,
        'swing_speed': swing_speed,
        'extend_speed': extend_speed,
        'counts': counts,
    }