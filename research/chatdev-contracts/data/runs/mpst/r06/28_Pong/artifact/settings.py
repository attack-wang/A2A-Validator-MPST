'''
settings.py
Central configuration: window dimensions, colors, entity sizes,
speeds, game rules and keyboard bindings for both players.
'''
import pygame
# Window
WIDTH, HEIGHT = 800, 600
CAPTION = "Two-Player Pong"
FPS = 60
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
# Paddle
PADDLE_WIDTH, PADDLE_HEIGHT = 12, 90
PADDLE_SPEED = 7
PADDLE_MARGIN = 20
# Ball
BALL_SIZE = 14
BALL_INITIAL_SPEED_X = 5
BALL_INITIAL_SPEED_Y = 3
BALL_SPEED_INCREMENT = 1
BALL_MAX_SPEED = 12
# Rules
WINNING_SCORE = 5
SERVE_DELAY_MS = 1000
# Key bindings
PLAYER1_KEYS = {"up": pygame.K_w, "down": pygame.K_s}
PLAYER2_KEYS = {"up": pygame.K_UP, "down": pygame.K_DOWN}