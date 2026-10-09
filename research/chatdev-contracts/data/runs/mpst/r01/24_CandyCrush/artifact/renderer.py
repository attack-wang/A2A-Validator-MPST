"""Draws everything: HUD, board, candies, effects, overlays."""
import math
import pygame
from settings import (...)
from utils import darken, lighten, star_points
from candy import Candy
from game import Game