'''
bitmaps.py
Pixel-art sprite patterns and a helper that converts a pattern (a list of
strings) into a pygame Surface. Using bitmaps keeps the game 100% code
generated - no external image assets are required.
'''
import pygame
# 'X' marks a filled pixel, '.' or ' ' marks a transparent pixel.
ALIEN_FRAMES = (
    ...
)
PLAYER_PATTERN = (...)
LIFE_ICON_PATTERN = (...)
def render_bitmap(pattern, color, pixel_size):
    ...