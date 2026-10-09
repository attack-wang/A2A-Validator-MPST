'''
Constants and configuration for the Space Invaders game.
'''
import pygame
# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Space Invaders"
# Colors (R, G, B)
BLACK = (10, 10, 20)
WHITE = (240, 240, 240)
GREEN = (80, 220, 100)
RED = (230, 80, 80)
CYAN = (80, 220, 220)
YELLOW = (240, 200, 60)
PURPLE = (180, 100, 240)
BLUE = (80, 130, 240)
GREY = (150, 150, 150)
# Game states
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_VICTORY = "victory"
# Ship
SHIP_SPEED = 5.0
SHIP_LIVES = 3
SHIP_WIDTH = 48
SHIP_HEIGHT = 32
SHIP_COOLDOWN = 18
INVINCIBLE_FRAMES = 90
# Bullets
BULLET_SPEED = 8.0
BULLET_WIDTH = 4
BULLET_HEIGHT = 14
ALIEN_BULLET_SPEED = 4.0
ALIEN_FIRE_CHANCE = 0.012
# Aliens
ALIEN_ROWS = 4
ALIEN_COLS = 8
ALIEN_WIDTH = 40
ALIEN_HEIGHT = 28
ALIEN_HORIZONTAL_SPACING = 12
ALIEN_VERTICAL_SPACING = 12
ALIEN_BASE_SPEED = 0.6
ALIEN_SPEEDUP_PER_KILL = 0.03
ALIEN_DROP_DISTANCE = 24
ALIEN_TOP_MARGIN = 70
ALIEN_LEFT_MARGIN = 60
ALIEN_ANIMATION_FRAMES = 30
# Colors per alien row (top -> bottom)
ALIEN_COLORS = [RED, PURPLE, CYAN, GREEN]
# Points per row (top row worth most)
ALIEN_ROW_POINTS = [30, 20, 20, 10]
# Wave clear bonus
WAVE_CLEAR_BONUS = 100
# Invasion line: aliens reaching this Y coordinate ends the game
INVASION_LINE_Y = SCREEN_HEIGHT - 80
# Fonts
FONT_NAME = None
FONT_SIZE_BIG = 64
FONT_SIZE_SMALL = 24