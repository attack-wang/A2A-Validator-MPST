"""Entry point for the Tower of the Sorcerer roguelike game.
Contains the Game class: pygame window, input handling (W/A/S/D),
movement/combat/chest/door logic, rendering (pre-rendered tile layer
plus UI panel), and the game-over/restart flow.
"""
import pygame
import config
from entities import Player
from map_generator import generate_level
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption(config.WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 14)
        self.big_font = pygame.font.SysFont("consolas", 32, bold=True)
        self.small_font = pygame.font.SysFont("consolas", 12)
        self.running = True
        self.reset()
    def reset(self):
        """Start a fresh run (level 1, full HP). Used by restart too."""
        self.level = 1
        self.player = Player(1, 1)
        self.encountered = []   # capped list of monster stats for the UI
        self.log = []           # capped message log
        self.game_over = False
        self.game_map = generate_level(self.level)
        self.player.x, self.player.y = self.game_map.start
        self._render_static_layer()
    # ---------------- input / logic ----------------
    def _log(self, msg):
        self.log.append(msg)
        if len(self.log) > 12:
            self.log.pop(0)
    def _record_encounter(self, stats_text):
        self.encountered.append(stats_text)
        if len(self.encountered) > 10:
            self.encountered.pop(0)
    def _try_move(self, dx, dy):
        """Core interaction logic. Order: wall -> monster -> chest -> door -> move."""
        if self.game_over:
            return
        tx, ty = self.player.x + dx, self.player.y + dy
        gm = self.game_map
        if not gm.is_floor(tx, ty):
            self._log("Blocked by wall.")
            return
        monster = gm.monster_at(tx, ty)
        if monster is not None:
            # Bump-to-fight: monster HP is subtracted from player HP.
            self.player.take_damage(monster.hp)
            self._record_encounter(monster.stats_text())
            self._log("Fought {} (-{} HP)".format(monster.name, monster.hp))
            gm.monsters.remove(monster)
            if not self.player.is_alive:
                self.player.hp = 0
                self.game_over = True
                self._log("You died! Press R to restart.")
            return  # player stays in place (bump combat)
        chest = gm.chest_at(tx, ty)
        if chest is not None:
            healed = chest.heal_amount
            self.player.heal(healed)
            gm.chests.remove(chest)
            self._log("Chest! +{} HP".format(healed))
        if (tx, ty) == gm.door:
            self.player.heal(config.LEVEL_CLEAR_BONUS)
            self.level += 1
            self._log("Floor cleared! Now floor {}.".format(self.level))
            self.game_map = generate_level(self.level)
            self.player.x, self.player.y = self.game_map.start
            self._render_static_layer()
            return
        self.player.x, self.player.y = tx, ty
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game_over:
                    self.reset()
                elif not self.game_over:
                    move = {
                        pygame.K_w: (0, -1),
                        pygame.K_a: (-1, 0),
                        pygame.K_s: (0, 1),
                        pygame.K_d: (1, 0),
                    }.get(event.key)
                    if move:
                        self._try_move(*move)
    # ---------------- rendering ----------------
    def _render_static_layer(self):
        """Pre-render walls/floors/door once per level (performance)."""
        layer = pygame.Surface((config.GRID_WIDTH * config.TILE_SIZE,
                                config.GRID_HEIGHT * config.TILE_SIZE))
        layer.fill(config.COLOR_BACKGROUND)
        for y in range(config.GRID_HEIGHT):
            for x in range(config.GRID_WIDTH):
                tile = self.game_map.tile_at(x, y)
                rect = pygame.Rect(x * config.TILE_SIZE, y * config.TILE_SIZE,
                                   config.TILE_SIZE, config.TILE_SIZE)
                if tile == config.TILE_WALL:
                    layer.fill(config.COLOR_WALL, rect)
                elif tile == config.TILE_DOOR:
                    layer.fill(config.COLOR_DOOR, rect)
                else:
                    layer.fill(config.COLOR_FLOOR, rect)
        self.static_layer = layer
    def _draw_panel(self):
        panel_rect = pygame.Rect(config.GRID_WIDTH * config.TILE_SIZE, 0,
                                 config.UI_PANEL_WIDTH, config.WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, config.COLOR_PANEL_BG, panel_rect)
        px = panel_rect.x + 12
        py = 14
        # Title
        title = self.font.render("Tower of the Sorcerer", True, config.COLOR_TITLE)
        self.screen.blit(title, (px, py)); py += 26
        floor_txt = self.font.render("Floor: {}".format(self.level), True, config.COLOR_PANEL_TEXT)
        self.screen.blit(floor_txt, (px, py)); py += 26
        # HP number + bar
        hp_txt = self.font.render("HP: {}".format(self.player.hp), True, config.COLOR_PANEL_TEXT)
        self.screen.blit(hp_txt, (px, py)); py += 22
        bar_rect = pygame.Rect(px, py, config.UI_PANEL_WIDTH - 24, 16)
        pygame.draw.rect(self.screen, config.COLOR_HP_BAR_BG, bar_rect)
        ratio = max(0.0, min(1.0, self.player.hp / config.PLAYER_START_HP))
        fg_w = int(bar_rect.width * ratio)
        if fg_w > 0:
            pygame.draw.rect(self.screen, config.COLOR_HP_BAR_FG,
                             (bar_rect.x, bar_rect.y, fg_w, bar_rect.height))
        py += 26
        # Encountered monsters
        enc_title = self.font.render("Monsters encountered:", True, config.COLOR_PANEL_TEXT)
        self.screen.blit(enc_title, (px, py)); py += 22
        for line in self.encountered:
            self.screen.blit(self.small_font.render(line, True, config.COLOR_PANEL_TEXT), (px, py))
            py += 16
        py += 10
        # Message log
        log_title = self.font.render("Log:", True, config.COLOR_PANEL_TEXT)
        self.screen.blit(log_title, (px, py)); py += 22
        for line in self.log:
            self.screen.blit(self.small_font.render(line, True, config.COLOR_LOG_TEXT), (px, py))
            py += 16
    def _draw(self):
        self.screen.fill(config.COLOR_BACKGROUND)
        self.screen.blit(self.static_layer, (0, 0))
        ts = config.TILE_SIZE
        # Chests
        for c in self.game_map.chests:
            rect = pygame.Rect(c.x * ts, c.y * ts, ts, ts)
            pygame.draw.rect(self.screen, config.COLOR_CHEST, rect)
        # Monsters
        for m in self.game_map.monsters:
            rect = pygame.Rect(m.x * ts, m.y * ts, ts, ts)
            pygame.draw.rect(self.screen, config.COLOR_MONSTER, rect)
        # Player
        prect = pygame.Rect(self.player.x * ts, self.player.y * ts, ts, ts)
        pygame.draw.rect(self.screen, config.COLOR_PLAYER, prect)
        self._draw_panel()
        if self.game_over:
            overlay = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(config.COLOR_OVERLAY)
            self.screen.blit(overlay, (0, 0))
            go = self.big_font.render("GAME OVER", True, (255, 80, 80))
            rs = self.font.render("Press R to restart, ESC to quit", True, config.COLOR_PANEL_TEXT)
            self.screen.blit(go, go.get_rect(center=(config.WINDOW_WIDTH // 2,
                                                     config.WINDOW_HEIGHT // 2 - 20)))
            self.screen.blit(rs, rs.get_rect(center=(config.WINDOW_WIDTH // 2,
                                                     config.WINDOW_HEIGHT // 2 + 30)))
    def run(self):
        while self.running:
            self._handle_events()
            self._draw()
            pygame.display.flip()
            self.clock.tick(config.FPS)
        pygame.quit()
if __name__ == "__main__":
    Game().run()