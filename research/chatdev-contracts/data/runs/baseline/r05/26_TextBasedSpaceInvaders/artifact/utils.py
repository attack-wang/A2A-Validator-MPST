import pygame
def bitmap_to_surface(bitmap, color, scale):
    """Build a surface from a list of strings ('X' = filled)."""
    rows = len(bitmap)
    cols = len(bitmap[0])
    surface = pygame.Surface((cols * scale, rows * scale), pygame.SRCALPHA)
    for r, line in enumerate(bitmap):
        for c, ch in enumerate(line):
            if ch == 'X':
                pygame.draw.rect(surface, color, (c * scale, r * scale, scale, scale))
    return surface