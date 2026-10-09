'''
assets.py
Utility helpers that build sprite images from small pixel-art patterns so the
game needs no external image files.
'''
SHIP_PATTERN = [
    "......X......",
    ".....XXX.....",
    ".....XXX.....",
    ".XXXXXXXXXXX.",
    "XXXXXXXXXXXXX",
    "XXXXXXXXXXXXX",
]
ALIEN_PATTERN = [
    "..X.....X..",
    "...X...X...",
    "..XXXXXXX..",
    ".XX.XXX.XX.",
    "XXXXXXXXXXX",
    "X.XXXXXXX.X",
    "X.X.....X.X",
    "...XX.XX...",
]
def image_from_pattern(pattern, color, scale=3):
    '''Build a pygame Surface from a text pattern. 'X' cells are filled with color.'''
    import pygame
    rows = len(pattern)
    cols = len(pattern[0])
    width = cols * scale
    height = rows * scale
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    for r, line in enumerate(pattern):
        for c, ch in enumerate(line):
            if ch == 'X':
                rect = pygame.Rect(c * scale, r * scale, scale, scale)
                pygame.draw.rect(surf, color, rect)
    return surf