'''
game_logic.py
Core game logic for 2048: grid state, tile movement/merging, spawning, scoring and game-over detection.
'''
import random
GRID_SIZE = 4  # hmm, better to import from constants
from constants import GRID_SIZE