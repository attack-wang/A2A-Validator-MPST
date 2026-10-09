'''
settings.py
Central configuration for the simplified Space Invaders game.
All tunable numbers live here: window size, colors, entity speeds,
fleet layout, scoring values and gameplay limits.
'''
# Window / loop
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WINDOW_TITLE = "Space Invaders - Simplified"
# Colors (R, G, B)
COLOR_BACKGROUND = (8, 10, 28)
COLOR_GROUND = (40, 120, 60)
COLOR_SHIP = (60, 220, 120)
COLOR_SHIP_DIM = (30, 110, 60)
COLOR_ALIEN_ROW_A = (170, 80, 220)
COLOR_ALIEN_ROW_B = (80, 190, 255)
COLOR_BULLET = (255, 240, 150)
COLOR_ENEMY_BULLET = (255, 90, 90)
COLOR_TEXT = (235, 235, 235)
COLOR_TEXT_DIM = (150, 155, 175)
COLOR_ACCENT = (255, 200, 60)
# Player ship
SHIP_SPEED = 380.0
SHIP_COOLDOWN = 0.40
SHIP_WIDTH = 44
SHIP_HEIGHT = 30
# Bullets
BULLET_SPEED = 560.0
BULLET_WIDTH = 4
BULLET_HEIGHT = 14
MAX_PLAYER_BULLETS = 3
ENEMY_BULLET_SPEED = 230.0
ENEMY_BULLET_WIDTH = 4
ENEMY_BULLET_HEIGHT = 12
ENEMY_FIRE_CHANCE = 0.035
# Alien fleet
ALIEN_ROWS = 4
ALIEN_COLUMNS = 8
ALIEN_WIDTH = 40
ALIEN_HEIGHT = 28
FLEET_HORIZONTAL_SPEED = 55.0
FLEET_DROP_DISTANCE = 24
FLEET_SPEEDUP_MAX = 2.5
FLEET_MARGIN_X = 12
# Scoring / lives
POINTS_PER_ROW = (100, 80, 60, 40)
STARTING_LIVES = 3
# Fonts
FONT_SIZE_SMALL = 20
FONT_SIZE = 26
FONT_SIZE_BIG = 56