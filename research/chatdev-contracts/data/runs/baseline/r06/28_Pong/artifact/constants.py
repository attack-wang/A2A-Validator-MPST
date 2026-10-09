'''
constants.py
Global configuration constants for the two-player Pong game:
window settings, colors, paddle/ball physics, controls and fonts.
'''
import math
import pygame
# ---------------- Window ----------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WINDOW_TITLE = "Two-Player Pong"
# ---------------- Colors ----------------
BLACK = (18, 18, 24)
WHITE = (235, 235, 235)
GRAY = (110, 110, 120)
P1_COLOR = (80, 200, 255)    # Player 1 (left paddle)
P2_COLOR = (255, 130, 90)    # Player 2 (right paddle)
SCORE_COLOR = (200, 200, 210)
# ---------------- Paddle ----------------
PADDLE_WIDTH = 12
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7.0
PADDLE_MARGIN = 16           # distance from the side walls
# Player 1 (left) controls
P1_UP_KEY = pygame.K_w
P1_DOWN_KEY = pygame.K_s
# Player 2 (right) controls
P2_UP_KEY = pygame.K_UP
P2_DOWN_KEY = pygame.K_DOWN
# ---------------- Ball ----------------
BALL_SIZE = 14
BALL_INITIAL_SPEED_X = 6.0
BALL_INITIAL_SPEED_Y_MIN = -4.0
BALL_INITIAL_SPEED_Y_MAX = 4.0
BALL_INITIAL_SPEED_Y_RANGE = (BALL_INITIAL_SPEED_Y_MIN, BALL_INITIAL_SPEED_Y_MAX)
BALL_SPEED_INCREMENT = 0.4   # speed gained on every paddle hit
BALL_MAX_SPEED = 15.0
BALL_MAX_BOUNCE_ANGLE = math.radians(60)  # steepest bounce off a paddle
# ---------------- Scoring ----------------
WINNING_SCORE = 5            # first player to reach this wins
SERVE_DELAY_FRAMES = 60      # 1 second pause after each point
# ---------------- Fonts ----------------
SCORE_FONT_SIZE = 52
MESSAGE_FONT_SIZE = 36
SMALL_FONT_SIZE = 22