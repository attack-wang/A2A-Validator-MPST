class MapGenerator:
    """Generates connected floors and guarantees a start->door path."""
    def generate(self, level, player_hp):
        """Produce a GameMap for the given level, or a safe fallback."""
        for _ in range(50):
            grid, rooms = self._carve_rooms_and_corridors()
            if grid is None:
                continue
            start, door, path = self._pick_start_and_door(grid, rooms)
            if path is None or len(path) < config.MIN_START_DOOR_DISTANCE:
                continue
            monsters, chests = self._place_entities(grid, path, level, player_hp)
            return GameMap(grid, start, door, monsters, chests)
        return self._fallback_map(level)