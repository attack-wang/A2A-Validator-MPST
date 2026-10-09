'''
main.py
Entry point of the Tower of the Sorcerer roguelike game.
Initialises pygame, creates the window, runs the main loop,
handles W/A/S/D input, renders the 80x80 map, entities and
the minimal UI panel (player HP, monster stats, message log).
'''
import sys
import pygame
import game_constants as C
from game_engine import GameEngine
def draw_text(surface, font, text, x, y, color=C.COLOR_UI_TEXT):
    """Blit a rendered text string onto the surface at (x, y)."""
    surface.blit(font.render(text, True, color), (x, y))
def draw_hp_bar(surface, x, y, w, h, hp, max_hp):
    """Draw a simple HP bar with a border."""
    pygame.draw.rect(surface, C.COLOR_HP_BAR_BACK, (x, y, w, h))
    if max_hp > 0:
        fill_w = int(w * hp / max_hp)
        pygame.draw.rect(surface, C.COLOR_HP_BAR_FILL, (x, y, fill_w, h))
    pygame.draw.rect(surface, C.COLOR_UI_TEXT, (x, y, w, h), 1)
def render(engine, screen, font, small_font):
    """Draw the whole frame: map, entities, UI panel and overlays."""
    screen.fill(C.COLOR_BG)
    game_map = engine.game_map
    # ---- map tiles ----
    for y in range(C.GRID_SIZE):
        row = game_map.grid[y]
        for x in range(C.GRID_SIZE):
            rect = pygame.Rect(x * C.TILE_SIZE, y * C.TILE_SIZE,
                               C.TILE_SIZE, C.TILE_SIZE)
            if row[x] == C.TILE_WALL:
                pygame.draw.rect(screen, C.COLOR_WALL, rect)
                pygame.draw.rect(screen, C.COLOR_WALL_EDGE, rect, 1)
            else:
                color = C.COLOR_FLOOR if (x + y) % 2 == 0 else C.COLOR_FLOOR_ALT
                pygame.draw.rect(screen, color, rect)
    # ---- treasure chests ----
    for chest in game_map.chests:
        rect = pygame.Rect(chest.x * C.TILE_SIZE + 1, chest.y * C.TILE_SIZE + 1,
                           C.TILE_SIZE - 2, C.TILE_SIZE - 2)
        pygame.draw.rect(screen, C.COLOR_CHEST, rect)
        pygame.draw.rect(screen, C.COLOR_CHEST_EDGE, rect, 1)
    # ---- monsters ----
    for monster in game_map.monsters:
        rect = pygame.Rect(monster.x * C.TILE_SIZE + 1, monster.y * C.TILE_SIZE + 1,
                           C.TILE_SIZE - 2, C.TILE_SIZE - 2)
        pygame.draw.rect(screen, monster.color, rect)
        pygame.draw.rect(screen, C.COLOR_OVERLAY, rect, 1)
    # ---- door ----
    door = game_map.door
    rect = pygame.Rect(door.x * C.TILE_SIZE, door.y * C.TILE_SIZE,
                       C.TILE_SIZE, C.TILE_SIZE)
    pygame.draw.rect(screen, C.COLOR_DOOR, rect)
    pygame.draw.rect(screen, C.COLOR_DOOR_EDGE, rect, 1)
    # ---- player ----
    player = engine.player
    rect = pygame.Rect(player.x * C.TILE_SIZE + 1, player.y * C.TILE_SIZE + 1,
                       C.TILE_SIZE - 2, C.TILE_SIZE - 2)
    pygame.draw.rect(screen, C.COLOR_PLAYER, rect)
    pygame.draw.rect(screen, C.COLOR_PLAYER_EDGE, rect, 1)
    # ---- UI panel ----
    px = C.MAP_PIXEL_SIZE
    pygame.draw.rect(screen, C.COLOR_UI_BG,
                     (px, 0, C.UI_PANEL_WIDTH, C.WINDOW_HEIGHT))
    draw_text(screen, font, C.WINDOW_TITLE, px + 16, 16, C.COLOR_UI_ACCENT)
    draw_text(screen, font, f"Floor {engine.level}", px + 16, 48)
    draw_text(screen, small_font, "HP", px + 16, 88)
    draw_hp_bar(screen, px + 48, 88, 180, 18, player.hp, player.max_hp)
    draw_text(screen, small_font, f"{player.hp}/{player.max_hp}", px + 16, 112)
    draw_text(screen, small_font,
              f"Monsters slain: {engine.monsters_defeated}", px + 16, 140)
    draw_text(screen, small_font,
              f"Chests opened: {engine.chests_opened}", px + 16, 160)
    if engine.last_monster:
        draw_text(screen, small_font, "Last monster:",
                  px + 16, 192, C.COLOR_UI_ACCENT)
        draw_text(screen, small_font, engine.last_monster["name"], px + 16, 212)
        draw_text(screen, small_font,
                  f"HP {engine.last_monster['hp']}/{engine.last_monster['max_hp']}",
                  px + 16, 230)
    draw_text(screen, small_font, "Messages:", px + 16, 262, C.COLOR_UI_ACCENT)
    for i, msg in enumerate(engine.messages):
        draw_text(screen, small_font, msg, px + 16, 282 + i * 18)
    draw_text(screen, small_font, "W/A/S/D move | R restart | ESC quit",
              px + 16, C.WINDOW_HEIGHT - 30)
    if engine.game_over:
        overlay = pygame.Surface((C.MAP_PIXEL_SIZE, C.WINDOW_HEIGHT),
                                 pygame.SRCALPHA)
        overlay.fill((*C.COLOR_OVERLAY, 180))
        screen.blit(overlay, (0, 0))
        draw_text(screen, font, "GAME OVER", 330, 370, C.COLOR_HP_BAR_FILL)
        draw_text(screen, small_font, "Press R to restart", 340, 410)
def main():
    """Create the window and run the game loop until the user quits."""
    pygame.init()
    screen = pygame.display.set_mode((C.WINDOW_WIDTH, C.WINDOW_HEIGHT))
    pygame.display.set_caption(C.WINDOW_TITLE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)
    small_font = pygame.font.SysFont(None, 20)
    engine = GameEngine()
    key_map = {
        pygame.K_w: "w",
        pygame.K_a: "a",
        pygame.K_s: "s",
        pygame.K_d: "d",
    }
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    engine.restart()
                elif not engine.game_over and event.key in key_map:
                    engine.move(key_map[event.key])
        render(engine, screen, font, small_font)
        pygame.display.flip()
        clock.tick(C.FPS)
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()