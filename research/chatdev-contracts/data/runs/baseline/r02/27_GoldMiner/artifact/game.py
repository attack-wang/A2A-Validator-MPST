'''
game.py
Core game orchestration: states, level flow, scoring, rendering.
'''
import math, random
import pygame
from settings import *
from claw import Claw
from level import generate_level
from ui import draw_hud, draw_text_center, FloatingText... 