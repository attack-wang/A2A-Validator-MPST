'''
game.py
Core game logic for the Flappy Bird clone (tkinter edition): state machine,
pipe spawning, difficulty scaling, collisions, scoring and rendering.
'''
import math
import random
import tkinter as tk
import settings
from bird import Bird
from pipe import Pipe
from utils import draw_text  # maybe not needed; canvas text has built-in centering
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"