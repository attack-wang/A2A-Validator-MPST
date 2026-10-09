'''
renderer.py
Draws the game: pre-rendered static map layer, entities, and the UI panel.
'''
import pygame
import settings
_map_cache = {"version": None, "surface": None}
def draw(screen, game, fonts):
    '''Render the whole frame: map, entities, UI and overlays.'''
    title_font, normal_font, small_font, tile_font = fonts
    screen.fill(settings.COLOR_UI_BG)
    map_surface = _get_map_surface(game)
    screen.blit(map_surface, (0, 0))
    _draw_door(screen, game)
    _draw_chests(screen, game)
    _draw_monsters(screen, game, tile_font)
    _draw_player(screen, game, tile_font)
    _draw_ui(screen, game, fonts)
    if game.game_over:
        _draw_game_over(screen, game, fonts)
    pygame.display.flip()
def _tile_rect(x, y):
    return pygame.Rect(x * settings.TILE_SIZE, y * settings.TILE_SIZE,
                       settings.TILE_SIZE, settings.TILE_SIZE)
def _get_map_surface(game):
    '''Build (once per floor) the static layer holding walls and floors.'''
    if _map_cache["version"] == game.map_version:
        return _map_cache["surface"]
    width = settings.GRID_WIDTH * settings.TILE_SIZE
    height = settings.GRID_HEIGHT * settings.TILE_SIZE
    surface = pygame.Surface((width, height))
    surface.fill(settings.COLOR_WALL)
    for y in range(settings.GRID_HEIGHT):
        for x in range(settings.GRID_WIDTH):
            if game.game_map.grid[y][x] == settings.FLOOR:
                surface.fill(settings.COLOR_FLOOR, _tile_rect(x, y))
    # mark the start tile so the player can orient themselves
    sx, sy = game.game_map.start
    surface.fill(settings.COLOR_START, _tile_rect(sx, sy))
    _map_cache["version"] = game.map_version
    _map_cache["surface"] = surface
    return surface
def _draw_door(screen, game):
    door = game.game_map.door
    rect = _tile_rect(door.x, door.y)
    pygame.draw.rect(screen, settings.COLOR_DOOR, rect, border_radius=2)
    # small inner frame to make the door stand out
    inner = rect.inflate(-4, -4)
    pygame.draw.rect(screen, settings.COLOR_UI_PANEL, inner, 1, border_radius=2)
def _draw_chests(screen, game):
    for chest in game.game_map.chests:
        rect = _tile_rect(chest.x, chest.y).inflate(-3, -3)
        pygame.draw.rect(screen, settings.COLOR_CHEST, rect, border_radius=2)
        pygame.draw.rect(screen, settings.COLOR_UI_PANEL, rect, 1, border_radius=2)
def _draw_monsters(screen, game, tile_font):
    for monster in game.game_map.monsters:
        rect = _tile_rect(monster.x, monster.y)
        pygame.draw.rect(screen, monster.color, rect.inflate(-2, -2),
                         border_radius=3)
        letter = tile_font.render(monster.name[0].upper(), True,
                                  settings.COLOR_TEXT)
        screen.blit(letter, letter.get_rect(center=rect.center))
def _draw_player(screen, game, tile_font):
    rect = _tile_rect(game.player.x, game.player.y)
    pygame.draw.rect(screen, settings.COLOR_PLAYER, rect.inflate(-2, -2),
                     border_radius=3)
    glyph = tile_font.render("@", True, settings.COLOR_UI_PANEL)
    screen.blit(glyph, glyph.get_rect(center=rect.center))