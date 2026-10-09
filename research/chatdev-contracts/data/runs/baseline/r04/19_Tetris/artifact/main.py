def draw_hud(self, game):
    """Draw score / level / lines and a controls legend in the side panel."""
    ox, oy = self._board_origin()
    panel_x = ox + BOARD_WIDTH * CELL_SIZE + MARGIN
    y = oy + 180
    for label, value in (('SCORE', game.score), ('LEVEL', game.level), ('LINES', game.lines)):
        self.screen.blit(self.font_small.render(label, True, COLOR_TEXT), (panel_x, y))
        self.screen.blit(self.font_medium.render(str(value), True, COLOR_TEXT), (panel_x, y + 26))
        y += 80
    # Controls legend
    controls = [
        'LEFT/RIGHT: move',
        'DOWN: soft drop',
        'UP: rotate',
        'SPACE: hard drop',
        'P: pause  R: restart',
    ]
    y += 10
    for line in controls:
        self.screen.blit(self.font_small.render(line, True, COLOR_TEXT), (panel_x, y))
        y += 24