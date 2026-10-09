"""Rendering: background, world objects, claw, HUD, and message screens."""
import math
import pygame
import config
class Renderer:
    def __init__(self):
        pygame.font.init()
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_large = pygame.font.Font(None, 56)
        self.font_huge = pygame.font.Font(None, 72)
        self.background = self._make_background()
    def _make_background(self):
        bg = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        bg.fill(config.COLOR_BG)
        # sky band above ground
        sky = pygame.Rect(0, 0, config.SCREEN_WIDTH, config.GROUND_Y)
        bg.fill((35, 48, 66), sky)
        # ground strip
        ground = pygame.Rect(0, config.GROUND_Y, config.SCREEN_WIDTH, config.MINING_TOP - config.GROUND_Y)
        bg.fill(config.COLOR_GROUND, ground)
        # dirt area with darker speckles
        dirt = pygame.Rect(0, config.MINING_TOP, config.SCREEN_WIDTH, config.SCREEN_HEIGHT - config.MINING_TOP)
        bg.fill(config.COLOR_DIRT, dirt)
        import random
        for _ in range(120):
            x = random.randint(config.MINING_LEFT, config.MINING_RIGHT - 4)
            y = random.randint(config.MINING_TOP, config.MINING_BOTTOM - 4)
            pygame.draw.rect(bg, config.COLOR_DIRT_DARK, (x, y, random.randint(3, 8), random.randint(2, 5)))
        # mining boundary lines
        pygame.draw.line(bg, config.COLOR_DIRT_DARK, (config.MINING_LEFT, config.MINING_TOP), (config.MINING_RIGHT, config.MINING_TOP), 2)
        return bg
    def draw_world(self, surface, level, claw, effects):
        surface.blit(self.background, (0, 0))
        for obj in level.objects:
            obj.draw(surface)
        claw.draw(surface)
        for effect in effects:
            effect.draw(surface)
    def draw_hud(self, surface, level, time_left):
        hud = pygame.Rect(0, 0, config.SCREEN_WIDTH, config.HUD_HEIGHT)
        pygame.draw.rect(surface, config.COLOR_HUD_BG, hud)
        pygame.draw.line(surface, config.COLOR_GOLD, (0, config.HUD_HEIGHT - 2), (config.SCREEN_WIDTH, config.HUD_HEIGHT - 2), 2)
        level_text = self.font_medium.render(f"Level {level.number}", True, config.COLOR_TEXT)
        surface.blit(level_text, (20, 12))
        goal_text = self.font_small.render(f"Goal: {level.gold_collected} / {level.target_gold}", True, config.COLOR_GOOD)
        surface.blit(goal_text, (20, 40))
        time_color = config.COLOR_TEXT if time_left > 10 else config.COLOR_BAD
        time_text = self.font_medium.render(f"Time: {max(0, int(time_left))}", True, time_color)
        surface.blit(time_text, (config.SCREEN_WIDTH - time_text.get_width() - 20, 12))
        # progress bar
        bar_x, bar_y, bar_w, bar_h = 220, 20, 300, 14
        pygame.draw.rect(surface, (25, 30, 40), (bar_x, bar_y, bar_w, bar_h), border_radius=4)
        progress = 0
        if level.target_gold > 0:
            progress = min(1.0, level.gold_collected / level.target_gold)
        fill_w = int(bar_w * progress)
        if fill_w > 0:
            pygame.draw.rect(surface, config.COLOR_GOLD, (bar_x, bar_y, fill_w, bar_h), border_radius=4)
        pygame.draw.rect(surface, config.COLOR_TEXT, (bar_x, bar_y, bar_w, bar_h), 2, border_radius=4)
        target_label = self.font_small.render("Gold progress", True, config.COLOR_TEXT)
        surface.blit(target_label, (bar_x, bar_y + bar_h + 4))
    def draw_message_screen(self, surface, title, lines, footer):
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 12, 18, 180))
        surface.blit(overlay, (0, 0))
        t = self.font_huge.render(title, True, config.COLOR_GOLD)
        surface.blit(t, (config.SCREEN_WIDTH // 2 - t.get_width() // 2, 170))
        y = 260
        for line in lines:
            s = self.font_medium.render(line, True, config.COLOR_TEXT)
            surface.blit(s, (config.SCREEN_WIDTH // 2 - s.get_width() // 2, y))
            y += 36
        f = self.font_small.render(footer, True, config.COLOR_GOOD)
        surface.blit(f, (config.SCREEN_WIDTH // 2 - f.get_width() // 2, config.SCREEN_HEIGHT - 90))