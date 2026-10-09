'''Configuration constants for the simplified Space Invaders game.'''
# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Space Invaders"
# Colors (R, G, B)
COLOR_BACKGROUND = (10, 10, 30)
COLOR_SHIP = (0, 200, 255)
COLOR_BULLET = (255, 255, 255)
COLOR_ALIEN_BOMB = (255, 80, 80)
COLOR_TEXT = (240, 240, 240)
COLOR_UI = (180, 180, 180)
# Ship
SHIP_SPEED = 320.0          # pixels per second
SHIP_WIDTH = 44
SHIP_HEIGHT = 28
SHIP_COOLDOWN = 0.35        # seconds between shots
SHIP_START_LIVES = 3
# Bullets
BULLET_SPEED = 520.0
BULLET_WIDTH = 4
BULLET_HEIGHT = 14
BOMB_SPEED = 220.0
BOMB_WIDTH = 5
BOMB_HEIGHT = 12
# Aliens
ALIEN_ROWS = 5
ALIEN_COLS = 8
ALIEN_WIDTH = 36
ALIEN_HEIGHT = 24
ALIEN_HORIZONTAL_SPEED = 40.0   # starting speed, pixels per second
ALIEN_DESCENT_STEP = 18         # pixels dropped on edge bounce
ALIEN_SPEEDUP = 1.04            # speed multiplier each time fleet bounces
ALIEN_FIRE_CHANCE = 0.6         # average bombs per second from fleet
ALIEN_BOTTOM_LIMIT = SCREEN_HEIGHT - 90  # y that triggers game over
# Scoring
ALIEN_POINTS_BY_ROW = [30, 25, 20, 15, 10]  # top row worth most