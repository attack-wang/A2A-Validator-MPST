'''Procedurally generated sprites for the bird and pipes (no image files needed).'''
import pygame
def create_bird_frames(width=44, height=36):
    """Build three bird frames (wing up, mid, down) for flap animation."""
    frames = []
    body_color = (255, 204, 61)
    body_outline = (150, 108, 24)
    belly_color = (255, 236, 160)
    wing_color = (255, 245, 220)
    wing_outline = (150, 108, 24)
    beak_color = (255, 90, 40)
    beak_outline = (170, 50, 20)
    eye_white = (255, 255, 255)
    eye_black = (40, 40, 40)
    for wing_pos in (-1, 0, 1):  # up, mid, down
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        # body
        pygame.draw.ellipse(surf, body_color, (2, 4, width - 6, height - 8))
        pygame.draw.ellipse(surf, body_outline, (2, 4, width - 6, height - 8), 2)
        # belly
        pygame.draw.ellipse(surf, belly_color, (6, height - 16, width - 14, 10))
        # wing
        wing_y = height // 2 - 6 + wing_pos * 5
        pygame.draw.ellipse(surf, wing_color, (8, wing_y, 18, 10))
        pygame.draw.ellipse(surf, wing_outline, (8, wing_y, 18, 10), 1)
        # eye
        pygame.draw.circle(surf, eye_white, (width - 14, 12), 6)
        pygame.draw.circle(surf, eye_black, (width - 12, 12), 3)
        # beak
        pygame.draw.polygon(surf, beak_color, [(width - 8, 16), (width - 1, 20), (width - 8, 24)])
        pygame.draw.polygon(surf, beak_outline, [(width - 8, 16), (width - 1, 20), (width - 8, 24)], 1)
        frames.append(surf)
    return frames
def create_pipe_body(width, height):
    """Build a green pipe body segment with shading stripes."""
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    body_color = (95, 190, 75)
    light_color = (140, 220, 110)
    dark_color = (55, 140, 50)
    outline_color = (35, 95, 35)
    pygame.draw.rect(surf, body_color, (0, 0, width, height))
    pygame.draw.rect(surf, light_color, (4, 0, 10, height))   # highlight stripe
    pygame.draw.rect(surf, dark_color, (width - 14, 0, 10, height))  # shadow stripe
    pygame.draw.rect(surf, outline_color, (0, 0, width, height), 2)
    return surf
def create_pipe_cap(width, height):
    """Build the wider lip/cap drawn at the gap-facing end of each pipe."""
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    body_color = (95, 190, 75)
    light_color = (140, 220, 110)
    dark_color = (55, 140, 50)
    outline_color = (35, 95, 35)
    pygame.draw.rect(surf, body_color, (0, 0, width, height))
    pygame.draw.rect(surf, light_color, (6, 0, 12, height))
    pygame.draw.rect(surf, dark_color, (width - 18, 0, 12, height))
    pygame.draw.rect(surf, outline_color, (0, 0, width, height), 2)
    return surf