SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
FPS = 60
# Colors
COLOR_SKY = (135, 206, 235)
COLOR_DIRT = (139, 90, 43)
COLOR_DIRT_DARK = (110, 70, 33)
COLOR_GRASS = (60, 160, 60)
COLOR_GOLD = (255, 200, 40)
COLOR_GOLD_DARK = (200, 150, 20)
COLOR_ROCK = (130, 130, 130)
COLOR_ROCK_DARK = (90, 90, 90)
COLOR_DIAMOND = (120, 220, 255)
COLOR_BONE = (235, 225, 200)
COLOR_TNT = (200, 40, 40)
COLOR_BAG = (150, 100, 50)
COLOR_TEXT = (40, 30, 20)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_HUD_BG = (60, 40, 20)
COLOR_BAR_BG = (40, 30, 20)
COLOR_BAR_FILL = (255, 200, 40)
COLOR_BAR_OK = (80, 200, 80)
COLOR_CLAW = (60, 60, 70)
COLOR_ROPE = (90, 60, 30)
# Layout
PIVOT_X = SCREEN_WIDTH // 2
PIVOT_Y = 90
PLAY_AREA_LEFT = 40
PLAY_AREA_RIGHT = SCREEN_WIDTH - 40
PLAY_AREA_TOP = 140
PLAY_AREA_BOTTOM = SCREEN_HEIGHT - 90
HUD_HEIGHT = 70
BOTTOM_PANEL_HEIGHT = 60
# Claw
CLAW_MIN_LENGTH = 60
CLAW_MAX_LENGTH = 620
CLAW_EXTEND_SPEED = 520.0   # px/s
CLAW_RETRACT_SPEED_EMPTY = 620.0
CLAW_GRAB_RADIUS = 12
CLAW_SWING_RANGE_DEG = 75.0
CLAW_BASE_SWING_SPEED = 1.6   # rad/s
CLAW_MAX_SWING_SPEED = 3.2
CLAW_SWING_SPEED_PER_LEVEL = 0.12
# Object values / sizes
OBJECT_TYPES = {
    'gold_small':  {'radius': 12, 'value': 50,  'reel_time': 0.8},
    'gold_medium': {'radius': 18, 'value': 100, 'reel_time': 1.4},
    'gold_large':  {'radius': 26, 'value': 250, 'reel_time': 2.2},
    'rock_small':  {'radius': 14, 'value': 20,  'reel_time': 1.2},
    'rock_large':  {'radius': 24, 'value': 40,  'reel_time': 2.0},
    'diamond':     {'radius': 14, 'value': 600, 'reel_time': 1.0},
    'bone':        {'radius': 16, 'value': 15,  'reel_time': 1.0},
    'tnt':         {'radius': 18, 'value': 0,   'reel_time': 0.0},
    'mystery':     {'radius': 16, 'value': 0,   'reel_time': 1.2},  # value randomized on collect
}
MYSTERY_NOMINAL_VALUE = 150
MYSTERY_MIN = 50
MYSTERY_MAX = 500
TNT_BLAST_RADIUS = 90
# Level progression
LEVEL_BASE_TARGET = 500
LEVEL_TARGET_STEP = 250
LEVEL_BASE_TIME = 60.0
LEVEL_TIME_STEP = 3.0
LEVEL_MIN_TIME = 35.0
LEVEL_BONUS_PER_SECOND = 10  # time bonus on level complete