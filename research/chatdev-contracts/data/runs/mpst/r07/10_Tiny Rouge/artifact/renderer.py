'''
renderer.py
Console renderer for the roguelike (standard library only - no pygame).
Draws a viewport of the fixed 80x80 grid using ASCII characters:
  # wall, . floor, D door, @ player, $ chest, letters for monsters.
A viewport (instead of printing all 80 rows) keeps the display readable
in a normal terminal while the underlying map stays a fixed 80x80 grid.
'''
from config import (
    GRID_SIZE, VIEW_WIDTH, VIEW_HEIGHT,
    TILE_WALL, TILE_FLOOR, TILE_DOOR,
    SYM_WALL, SYM_FLOOR, SYM_DOOR, SYM_PLAYER, SYM_CHEST, SYM_UNKNOWN,
)
class Renderer:
    def __init__(self, view_width=VIEW_WIDTH, view_height=VIEW_HEIGHT):
        self.view_width = view_width
        self.view_height = view_height
    def render(self, game):
        '''Return the whole frame (map viewport + UI) as a string.'''
        lines = []
        lines.extend(self._render_map(game))
        return "\n".join(lines)
    def _viewport_origin(self, game):
        px, py = game.player.x, game.player.y
        x0 = px - self.view_width // 2
        y0 = py - self.view_height // 2
        x0 = max(0, min(x0, GRID_SIZE - self.view_width))
        y0 = max(0, min(y0, GRID_SIZE - self.view_height))
        return x0, y0
    def _render_map(self, game):
        x0, y0 = self._viewport_origin(game)
        # build lookup dicts for entities inside the viewport
        monsters = {(m.x, m.y): m for m in game.monsters}
        chests = {(c.x, c.y): c for c in game.chests}
        lines = []
        for y in range(y0, y0 + self.view_height):
            row = []
            for x in range(x0, x0 + self.view_width):
                row.append(self._tile_symbol(game, x, y, monsters, chests))
            lines.append("".join(row))
        return lines
    def _tile_symbol(self, game, x, y, monsters, chests):
        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
            return SYM_UNKNOWN
        if game.player.x == x and game.player.y == y:
            return SYM_PLAYER
        monster = monsters.get((x, y))
        if monster is not None:
            return monster.symbol
        if chests.get((x, y)) is not None:
            return SYM_CHEST
        tile = game.grid[y][x]
        if tile == TILE_WALL:
            return SYM_WALL
        if tile == TILE_DOOR:
            return SYM_DOOR
        return SYM_FLOOR