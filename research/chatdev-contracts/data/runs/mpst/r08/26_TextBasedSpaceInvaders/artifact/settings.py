'''
Global configuration constants for the simplified Space Invaders game.
'''
# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Space Invaders"
# Colors (R, G, B)
COLOR_BACKGROUND = (10, 10, 30)
COLOR_PLAYER = (0, 200, 255)
COLOR_ALIEN = [(255, 80, 80), (255, 160, 60), (255, 220, 80), (120, 220, 120), (120, 160, 255)]
COLOR_BULLET_PLAYER = (0, 255, 120)
COLOR_BULLET_ALIEN = (255, 80, 120)
COLOR_TEXT = (240, 240, 240)
COLOR_EXPLOSION = (255, 140, 0)
# Player
PLAYER_SPEED = 320.0          # pixels per second
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 24
PLAYER_START_LIVES = 3
PLAYER_RESPAWN_INVINCIBILITY = 1.5  # seconds
PLAYER_Y_OFFSET = 40          # distance from bottom of screen
# Player bullets
PLAYER_BULLET_SPEED = 480.0
PLAYER_BULLET_WIDTH = 4
PLAYER_BULLET_HEIGHT = 14
PLAYER_FIRE_COOLDOWN = 0.35   # seconds between shots
MAX_PLAYER_BULLETS = 3
# Alien fleet
ALIEN_ROWS = 5
ALIEN_COLUMNS = 10
ALIEN_WIDTH = 36
ALIEN_HEIGHT = 26
ALIEN_HORIZONTAL_SPACING = 12
ALIEN_VERTICAL_SPACING = 14
ALIEN_FLEET_TOP_OFFSET = 70
ALIEN_BASE_SPEED = 40.0       # pixels per second
ALIEN_SPEED_INCREMENT = 12.0  # speed added per destroyed alien
ALIEN_MAX_SPEED = 260.0
ALIEN_DROP_DISTANCE = 22      # pixels dropped on edge hit
ALIEN_FIRE_INTERVAL = 1.1     # average seconds between alien shots
MAX_ALIEN_BULLETS = 6
ALIEN_BULLET_SPEED = 220.0
ALIEN_BULLET_WIDTH = 4
ALIEN_BULLET_HEIGHT = 12
# Scoring: points per alien, from top row to bottom row
ALIEN_POINTS_PER_ROW = [30, 25, 20, 15, 10]
# Game over line: aliens reaching this y (from top) end the game
ALIEN_LOSE_LINE = SCREEN_HEIGHT - 120