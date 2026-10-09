'''
UI helpers: cached fonts and centered message rendering.
'''
import pygame
import settings
_font_cache = {}
def get_font(size):
    '''Return a cached pygame Font of the requested size.'''
    if size not in _font_cache:
        _font_cache[size] = pygame.font.Font(None, size)
    return _font_cache[size]
def draw_center_message(surface, title, subtitle):
    '''Render a large title and smaller subtitle centered on the surface.'''
    title_surf = get_font(64).render(title, True, settings.COLOR_TEXT)
    sub_surf = get_font(28).render(subtitle, True, settings.COLOR_TEXT)
    surface.blit(title_surf, title_surf.get_rect(
        center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 - 30)))
    surface.blit(sub_surf, sub_surf.get_rect(
        center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + 30)))