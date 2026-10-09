"""Rendering: map surface caching, entity drawing, and UI panel."""
class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font_small = pygame.font.SysFont(...)
        self.font_big = ...
        self.map_surface = None
    def on_level_changed(self, grid): pre-render map surface
    def draw(self, game): blit map, draw entities, draw UI, overlays (game over)