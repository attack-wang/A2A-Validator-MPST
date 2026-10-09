def _draw_wrong_flag_cross(self, x, y):
    inset = CELL_SIZE * 0.25
    self.canvas.create_line(x + inset, y + inset, x + CELL_SIZE - inset, y + CELL_SIZE - inset, fill=WRONG_FLAG_X, width=3)
    self.canvas.create_line(x + CELL_SIZE - inset, y + inset, x + inset, y + CELL_SIZE - inset, fill=WRONG_FLAG_X, width=3)