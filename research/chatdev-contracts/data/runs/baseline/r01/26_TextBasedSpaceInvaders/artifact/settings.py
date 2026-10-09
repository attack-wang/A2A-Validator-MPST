'''
settings.py
Contains all the configuration constants for the Space Invaders game.
'''
# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
SCREEN_TITLE = "Space Invaders"
BG_COLOR = (10, 10, 30)
# Ship settings
SHIP_SPEED = 6.0
SHIP_LIMIT = 3  # number of lives
# Bullet settings (player)
BULLET_SPEED = 8.0
BULLET_WIDTH = 4
BULLET_HEIGHT = 14
BULLET_COLOR = (60, 220, 60)
BULLET_COOLDOWN = 300  # milliseconds between shots
# Alien bomb settings
BOMB_SPEED = 4.0
BOMB_WIDTH = 4
BOMB_HEIGHT = 12
BOMB_COLOR = (220, 60, 60)
ALIEN_FIRE_CHANCE = 0.02  # chance per frame that an alien drops a bomb
# Alien fleet settings
ALIEN_ROWS = 4
ALIEN_COLUMNS = 8
ALIEN_SPEED_X = 1.0
FLEET_DROP_SPEED = 20
POINTS_PER_ALIEN = 10
ALIEN_POINTS_INCREMENT = 5  # extra points per wave cleared
# Colors
WHITE = (240, 240, 240)
GREEN = (80, 220, 80)