class MapGenerator:
    MAX_GENERATION_ATTEMPTS = 20
    def generate(self, level):
        for _ in range(self.MAX_GENERATION_ATTEMPTS):
            grid, start, door = self._carve()
            game_map = GameMap(level, grid, start, door, [], [])
            reachable = game_map.reachable_from(start)
            if door not in reachable:
                continue
            monsters, chests = self._place_entities(game_map, reachable, level)
            game_map.monsters = {m.position: m for m in monsters}
            game_map.chests = {c.position: c for c in chests}
            return game_map
        # Fallback (practically unreachable): open border-to-border corridor
        ...