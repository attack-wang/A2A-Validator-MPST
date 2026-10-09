def randomize_position(self, snake_positions):
    """Place food on a random grid cell not occupied by the snake."""
    occupied = set(snake_positions)
    free_cells = [
        (x, y)
        for x in range(GRID_WIDTH)
        for y in range(GRID_HEIGHT)
        if (x, y) not in occupied
    ]
    if free_cells:
        self.position = random.choice(free_cells)
    # If the board is completely full there is no free cell; the game's
    # victory check fires before this method is called, so the current
    # position is simply kept as a safe fallback.