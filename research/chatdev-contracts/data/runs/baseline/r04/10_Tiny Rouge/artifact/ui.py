'''Minimal text UI: renders the 80x80 map plus HP / monster status panel.'''
from settings import (GRID_WIDTH, GRID_HEIGHT, TILE_WALL, TILE_FLOOR, TILE_DOOR,
                      SYMBOL_WALL, SYMBOL_FLOOR, SYMBOL_DOOR, SYMBOL_PLAYER,
                      SYMBOL_MONSTER, SYMBOL_CHEST, VICTORY_LEVEL,
                      PLAYER_START_HP)
HP_BAR_WIDTH = 30
class UI:
    '''Builds the full console screen (map + side info) as a string.'''
    def render_screen(self, game):
        lines = []
        lines.append("=" * GRID_WIDTH)
        lines.append("  TOWER OF THE SORCERER   |   Floor {}/{}".format(game.level_num, VICTORY_LEVEL))
        lines.append("=" * GRID_WIDTH)
        lines.append("Legend: @=You  M=Monster  $=Chest  D=Door  #=Wall  .=Floor")
        lines.extend(self._map_lines(game))
        lines.extend(self._panel_lines(game))
        return "\n".join(lines) + "\n"
    def _map_lines(self, game):
        out = []
        px, py = game.player.pos
        for y in range(GRID_HEIGHT):
            chars = []
            row = game.grid[y]
            for x in range(GRID_WIDTH):
                if x == px and y == py:
                    chars.append(SYMBOL_PLAYER)
                elif (x, y) in game.monsters:
                    chars.append(SYMBOL_MONSTER)
                elif (x, y) in game.chests:
                    chars.append(SYMBOL_CHEST)
                else:
                    tile = row[x]
                    if tile == TILE_WALL:
                        chars.append(SYMBOL_WALL)
                    elif tile == TILE_DOOR:
                        chars.append(SYMBOL_DOOR)
                    else:
                        chars.append(SYMBOL_FLOOR)
            out.append("".join(chars))
        return out
    def _panel_lines(self, game):
        out = []
        out.append("-" * GRID_WIDTH)
        # HP bar
        ratio = max(0.0, min(1.0, game.player.hp / float(game.player.max_hp)))
        filled = int(round(ratio * HP_BAR_WIDTH))
        bar = "[" + "#" * filled + "." * (HP_BAR_WIDTH - filled) + "]"
        out.append("HP: {} {}/{}".format(bar, game.player.hp, game.player.max_hp))
        # Encountered monster
        if game.encountered is not None:
            m = game.encountered
            if (m.x, m.y) in game.monsters:
                status = "blocking the way"
            elif game.state == "game_over":
                status = "it defeated you!"
            else:
                status = "defeated"
            out.append("Encountered Monster: {}  (HP: {})  [{}]".format(m.name, m.hp, status))
        else:
            out.append("Encountered Monster: (none yet)")
        # Monsters / chests remaining
        out.append("Monsters left: {}   Chests left: {}".format(len(game.monsters), len(game.chests)))
        out.append("-" * GRID_WIDTH)
        out.append("Controls: W/A/S/D = move   R = restart (after death/victory)   Q = quit")
        out.append("Log:")
        for msg in game.messages:
            out.append("  " + msg)
        if game.state == "game_over":
            out.append("*** GAME OVER ***  You died on floor {}. Press R to restart.".format(game.level_num))
        elif game.state == "victory":
            out.append("*** VICTORY! ***  You conquered all {} floors! Press R to play again.".format(VICTORY_LEVEL))
        return out