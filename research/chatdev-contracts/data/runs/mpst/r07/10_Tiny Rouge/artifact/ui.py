'''
ui.py
Minimal text UI (customer requirement):
- player HP bar + numeric HP
- current dungeon level
- stats of the last monster encountered
- short message log
- controls help
Pure standard library only - no pygame required.
'''
from config import HP_BAR_WIDTH, LOG_MAX_ENTRIES
from game import LOG_INFO, LOG_GOOD, LOG_BAD, LOG_EVENT
class UI:
    def render(self, game):
        '''Return the UI panel (HP, level, monster stats, log) as a string.'''
        lines = []
        lines.append("=" * 50)
        lines.append("TOWER OF THE SORCERER - ROGUELIKE")
        lines.append("=" * 50)
        lines.append("Level: {}".format(game.level))
        lines.append("HP: {} / {}  {}".format(
            game.player.hp, game.player.max_hp, self._hp_bar(game)))
        lines.append("-" * 50)
        if game.last_monster is not None:
            lines.append("Last monster: {}".format(game.last_monster.describe()))
        else:
            lines.append("Last monster: none yet")
        lines.append("Monsters left: {}   Chests left: {}".format(
            len(game.monsters), len(game.chests)))
        lines.append("-" * 50)
        lines.extend(self._log_lines(game))
        lines.append("-" * 50)
        lines.append("Move: W/A/S/D   Restart: R   Quit: Q or ESC")
        return "\n".join(lines)
    def _hp_bar(self, game):
        ratio = max(0.0, min(1.0, game.player.hp / float(game.player.max_hp)))
        filled = int(round(ratio * HP_BAR_WIDTH))
        return "[" + "#" * filled + "-" * (HP_BAR_WIDTH - filled) + "]"
    def _log_lines(self, game):
        lines = []
        for text, kind in game.log[-LOG_MAX_ENTRIES:]:
            prefix = {"info": "  ", "good": "+ ", "bad": "! ", "event": "* "}.get(kind, "  ")
            lines.append(prefix + text)
        return lines