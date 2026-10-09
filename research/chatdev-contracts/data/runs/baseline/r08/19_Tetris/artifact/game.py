import random  # no longer needed if using random_tetromino
from tetromino import random_tetromino
from board import Board
from constants import (BOARD_WIDTH, COLORS, LINE_SCORES, SOFT_DROP_POINTS,
                       HARD_DROP_POINTS, LINES_PER_LEVEL,
                       BASE_DROP_INTERVAL, MIN_DROP_INTERVAL, SPEED_FACTOR)