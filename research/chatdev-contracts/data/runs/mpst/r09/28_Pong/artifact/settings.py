'''
settings.py
Global configuration constants for the two-player Pong game:
screen dimensions, colors, entity sizes, speeds, controls and scoring rules.
'''
import pygame
# --- Window / loop ---------------------------------------------------------
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60
WINDOW_CAPTION = "Pong - Two Player"
# --- Colors (R, G, B) ------------------------------------------------------
COLOR_BACKGROUND = (15, 15, 25)
COLOR_TEXT = (230, 230, 230)
COLOR_CENTER_LINE = (80, 80, 105)
COLOR_BALL = (240, 240, 240)
COLOR_PADDLE_LEFT = (80, 170, 255)
COLOR_PADDLE_RIGHT = (255, 120, 90)
# --- Paddle ----------------------------------------------------------------
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7.0
PADDLE_MARGIN = 24          # distance between paddle and its side wall
# --- Ball ------------------------------------------------------------------
BALL_SIZE = 14
BALL_INITIAL_SPEED_X = 6.0
BALL_INITIAL_SPEED_Y = 4.0
BALL_MAX_SPEED = 14.0       # upper bound for total speed after speed-ups
BALL_SPEEDUP_FACTOR = 1.04  # speed multiplier applied on every paddle hit
BALL_MAX_BOUNCE_ANGLE = 60  # degrees; steepest vertical angle off a paddle
# --- Scoring ---------------------------------------------------------------
WINNING_SCORE = 5
# --- Controls --------------------------------------------------------------
CONTROLS_LEFT = {"up": pygame.K_w, "down": pygame.K_s}
CONTROLS_RIGHT = {"up": pygame.K_UP, "down": pygame.K_DOWN}