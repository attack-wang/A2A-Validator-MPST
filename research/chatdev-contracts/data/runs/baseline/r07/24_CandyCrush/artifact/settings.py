"""Global configuration constants for the match-3 puzzle game."""
import pygame
# --- Window ---
WINDOW_WIDTH = 780
WINDOW_HEIGHT = 660
FPS = 60
TITLE = "Candy Match — a match-3 puzzle game"
# --- Board ---
GRID_SIZE = 8
CELL_SIZE = 64
BOARD_X = 44
BOARD_Y = 96
BOARD_PIXELS = GRID_SIZE * CELL_SIZE
# --- Panel ---
PANEL_X = BOARD_X + BOARD_PIXELS + 28
PANEL_WIDTH = WINDOW_WIDTH - PANEL_X - 20
# --- Candies ---
NUM_CANDY_TYPES = 6
CANDY_NAMES = ["Cherry", "Orange", "Lemon", "Lime", "Blueberry", "Grape"]
CANDY_COLORS = [
    (220, 60, 60), (240, 150, 40), (240, 220, 60),
    (90, 200, 90), (80, 140, 240), (170, 100, 220),
]
CANDY_DARK_COLORS = [
    (150, 30, 30), (170, 95, 20), (170, 150, 20),
    (50, 135, 50), (40, 90, 170), (110, 55, 155),
]
# --- Gameplay ---
STARTING_MOVES = 30
BASE_MATCH_SCORE = 60
SCORE_PER_EXTRA_CANDY = 20
COMBO_MULTIPLIER_STEP = 0.5
FALL_SPEED = 900  # pixels per second
SWAP_SPEED = 480
SHUFFLE_PENALTY = 100
# --- UI colors ---
COLOR_BG = (24, 26, 38)
COLOR_PANEL = (36, 40, 58)
COLOR_BOARD_BG = (16, 18, 28)
COLOR_CELL = (30, 33, 48)
COLOR_TEXT = (230, 230, 235)
COLOR_SELECTED = (255, 255, 255)
COLOR_OVERLAY = (0, 0, 0, 160)