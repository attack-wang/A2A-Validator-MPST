def draw(self, surface):
    self._draw_pipe(surface, self.top_rect, cap_bottom=True)
    self._draw_pipe(surface, self.bottom_rect, cap_bottom=False)