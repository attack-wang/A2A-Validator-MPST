'''
Utility helpers: fonts, drawing primitives, math helpers.
'''
import math
import pygame
import settings
_font_cache = {}
def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))
def get_font(size, bold=True):
    key = (size, bold)
    if key not in _font_cache:
        font = pygame.font.SysFont("arial", size, bold=bold)
        _font_cache[key] = font
    return _font_cache[key]
def draw_text(surface, text, size, center_pos, color, shadow_color=None):
    font = get_font(size)
    label = font.render(text, True, color)
    rect = label.get_rect(center=center_pos)
    if shadow_color is not None:
        shadow = font.render(text, True, shadow_color)
        shadow_rect = rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        surface.blit(shadow, shadow_rect)
    surface.blit(label, rect)
def draw_bird(surface, x, y, rotation, wing_phase):
    """Draw a stylized bird (body, wing, eye, beak) rotated by rotation degrees."""
    body_radius = settings.BIRD_RADIUS
    bird_surface = pygame.Surface((body_radius * 4, body_radius * 4), pygame.SRCALPHA)
    cx = body_radius * 2
    cy = body_radius * 2
    # body
    pygame.draw.circle(bird_surface, settings.BIRD_BODY, (cx, cy), body_radius)
    pygame.draw.circle(bird_surface, settings.PIPE_OUTLINE, (cx, cy), body_radius, 2)
    # beak (points right)
    beak = [(cx + body_radius - 2, cy - 5), (cx + body_radius + 9, cy), (cx + body_radius - 2, cy + 5)]
    pygame.draw.polygon(bird_surface, settings.BIRD_BEAK, beak)
    # eye
    pygame.draw.circle(bird_surface, settings.CLOUD_COLOR, (cx + 5, cy - 6), 5)
    pygame.draw.circle(bird_surface, settings.BIRD_EYE, (cx + 7, cy - 6), 2)
    # wing (flaps with wing_phase)
    flap = math.sin(wing_phase)
    wing_y = cy + int(flap * 6)
    wing = [(cx - 10, cy), (cx + 2, wing_y - 4), (cx + 2, wing_y + 6)]
    pygame.draw.polygon(bird_surface, settings.BIRD_WING, wing)
    # rotate and blit
    rotated = pygame.transform.rotate(bird_surface, rotation)
    rect = rotated.get_rect(center=(int(x), int(y)))
    surface.blit(rotated, rect.topleft)
def draw_pipe_column(surface, rect):
    """Draw a pipe column with shading and outline."""
    pygame.draw.rect(surface, settings.PIPE_BODY, rect)
    # highlight strip on the left, shadow strip on the right
    pygame.draw.rect(surface, settings.PIPE_LIGHT, (rect.x + 4, rect.y, 10, rect.height))
    pygame.draw.rect(surface, settings.PIPE_DARK, (rect.right - 12, rect.y, 8, rect.height))
    pygame.draw.rect(surface, settings.PIPE_OUTLINE, rect, 2)
def draw_pipe_cap(surface, rect):
    """Draw the wider cap at the gap edge of a pipe."""
    pygame.draw.rect(surface, settings.PIPE_BODY, rect, border_radius=3)
    pygame.draw.rect(surface, settings.PIPE_LIGHT, (rect.x + 4, rect.y + 3, 10, rect.height - 6))
    pygame.draw.rect(surface, settings.PIPE_OUTLINE, rect, 2, border_radius=3)