def handle_space(self, player, depth=0):
    """Resolve whatever space the player currently occupies."""
    if depth > 3:  # safety guard against chained card movements
        return
    space = self.board.get_space(player.position)
    ...
    elif space.kind == "chance":
        self.handle_chance(player, depth)