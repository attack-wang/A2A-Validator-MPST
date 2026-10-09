'''
Configuration constants for the Snake game.
'''
# Grid dimensions (in cells)
GRID_WIDTH = 30
GRID_HEIGHT = 20
# Size of each cell in pixels
CELL_SIZE = 25
# Colors (hex)
COLOR_BACKGROUND = "#1e1e2e"
COLOR_GRID = "#2a2a3c"
COLOR_SNAKE_HEAD = "#a6e3a1"
COLOR_SNAKE_BODY = "#94e2d5"
COLOR_FOOD = "#f38ba8"
COLOR_TEXT = "#cdd6f4"
COLOR_BORDER = "#f5c2e7"
# Directions as (dx, dy) tuples
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
# Difficulty levels: name -> (move interval in ms, score per food)
DIFFICULTY_LEVELS = {
    "Easy": (200, 1),
    "Medium": (130, 2),
    "Hard": (80, 3),
    "Insane": (50, 5),
}
# Score file
SCORE_FILE = "highscores.json"