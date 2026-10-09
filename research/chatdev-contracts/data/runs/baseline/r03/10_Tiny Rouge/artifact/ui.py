'''
ui.py
Pygame front-end for the roguelike. Renders the 80x80 grid, the player,
monsters, chests and the door, plus a minimal HUD panel that shows the
player's current HP (with a bar), the current floor, and the stats of the
last encountered monster. Handles W/A/S/D movement, R for restart and
ESC to quit.
'''
import sys
import pygame
import config
from config import (WINDOW_WIDTH, WINDOW_HEIGHT, FPS, WINDOW_TITLE,
                    TILE_SIZE, HUD_HEIGHT, TILE_WALL, TILE_FLOOR, TILE_DOOR,
                    COLOR_BACKGROUND, COLOR_WALL, COLOR_FLOOR, COLOR_DOOR,
                    COLOR_CHEST, COLOR_CHEST_BORDER, COLOR_PLAYER,
                    COLOR_PLAYER_BORDER, COLOR_MONSTER_BORDER,
                    COLOR_HUD_BG, COLOR_HUD_TEXT, COLOR_HUD_TEXT_DIM,
                    COLOR_HUD_HP_BAR_BG, COLOR_HUD_HP_BAR_FG, COLOR_GAME_OVER)
class UI:
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.small_font = pygame.font.SysFont(None, 20)
        self.running = True
    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self._handle_key(event.key)
            self._draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit(0)
    def _handle_key(self, key):
        '''Translate W/A/S/D (and arrow keys as a convenience) into moves.'''
        mapping = {pygame.K_w: (0, -1),
                   pygame.K_s: (0, 1),
                   pygame.K_a: (-1, 0),
                   pygame.K_d: (1, 0)}
        if key in mapping:
            self.game.handle_move(*mapping[key])
        elif key == pygame.K_r:
            self.game.restart()
        elif key == pygame.K_ESCAPE:
            self.running = False
    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------
    def _draw(self):
        self.screen.fill(COLOR_BACKGROUND)
        self._draw_map()
        self._draw_hud()
        if self.game.game_over:
            self._draw_game_over()
    def _draw_map(self):
        grid = self.game.grid
        for y in range(config.GRID_HEIGHT):
            for x in range(config.GRID_WIDTH):
                tile = grid[y][x]
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE,
                                   TILE_SIZE, TILE_SIZE)
                if tile == TILE_WALL:
                    pygame.draw.rect(self.screen, COLOR_WALL, rect)
                elif tile == TILE_DOOR:
                    pygame.draw.rect(self.screen, COLOR_DOOR, rect)
                else:  # TILE_FLOOR
                    pygame.draw.rect(self.screen, COLOR_FLOOR, rect)
        for chest in self.game.chests:
            self._draw_entity(chest.x, chest.y, COLOR_CHEST, COLOR_CHEST_BORDER)
        for monster in self.game.monsters:
            self._draw_entity(monster.x, monster.y, monster.color,
                              COLOR_MONSTER_BORDER)
        self._draw_entity(self.game.player.x, self.game.player.y,
                          COLOR_PLAYER, COLOR_PLAYER_BORDER)
    def _draw_entity(self, x, y, color, border_color):
        pad = 1
        rect = pygame.Rect(x * TILE_SIZE + pad, y * TILE_SIZE + pad,
                           TILE_SIZE - 2 * pad, TILE_SIZE - 2 * pad)
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, border_color, rect, 1)
    def _draw_hud(self):
        hud_rect = pygame.Rect(0, WINDOW_HEIGHT - HUD_HEIGHT,
                               WINDOW_WIDTH, HUD_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_HUD_BG, hud_rect)
        player = self.game.player
        # HP bar
        bar_x, bar_y = 20, WINDOW_HEIGHT - HUD_HEIGHT + 20
        bar_w, bar_h = 300, 22
        pygame.draw.rect(self.screen, COLOR_HUD_HP_BAR_BG,
                         (bar_x, bar_y, bar_w, bar_h))
        ratio = 0.0
        if player is not None and player.max_hp > 0:
            ratio = max(0.0, min(1.0, player.hp / player.max_hp))
        pygame.draw.rect(self.screen, COLOR_HUD_HP_BAR_FG,
                         (bar_x, bar_y, int(bar_w * ratio), bar_h))
        hp_text = self.font.render(f"HP: {player.hp}/{player.max_hp}",
                                   True, COLOR_HUD_TEXT)
        self.screen.blit(hp_text, (bar_x + bar_w + 15, bar_y))
        floor_text = self.font.render(f"Floor: {self.game.level}",
                                      True, COLOR_HUD_TEXT)
        self.screen.blit(floor_text, (bar_x, bar_y + bar_h + 10))
        # Last encountered monster stats
        if self.game.last_monster is not None:
            monster_text = self.small_font.render(
                "Last monster: " + self.game.last_monster.stats_text(),
                True, COLOR_HUD_TEXT)
        else:
            monster_text = self.small_font.render(
                "Last monster: none yet (walk into a monster to fight)",
                True, COLOR_HUD_TEXT_DIM)
        self.screen.blit(monster_text, (bar_x + 340, bar_y + 2))
        # Message log
        for i, msg in enumerate(self.game.messages):
            msg_text = self.small_font.render(msg, True, COLOR_HUD_TEXT_DIM)
            self.screen.blit(msg_text, (bar_x + 340, bar_y + 26 + i * 20))
    def _draw_game_over(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT),
                                 pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        text = self.font.render("GAME OVER - Press R to restart",
                                True, COLOR_GAME_OVER)
        rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(text, rect)