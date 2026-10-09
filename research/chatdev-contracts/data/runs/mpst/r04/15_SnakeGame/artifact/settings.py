'''
Global settings and configuration constants for the Snake game.
'''
# Window / board configuration
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
HUD_HEIGHT = 40  # extra space at top for score display
# Colors (R, G, B)
COLORS = {
    "background": (18, 18, 18),
    "grid": (30, 30, 30),
    "snake_head": (0, 200, 80),
    "snake_body": (0, 150, 60),
    "food": (220, 40, 40),
    "text": (240, 240, 240),
    "hud_background": (10, 10, 10),
    "menu_background": (25, 25, 35),
    "highlight": (255, 200, 0),
    "victory": (80, 200, 255),
}
# Difficulty levels: name -> ticks per second (moves per second)
DIFFICULTY_LEVELS = {
    "Easy": 6,
    "Medium": 10,
    "Hard": 15,
    "Insane": 22,
}
# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)