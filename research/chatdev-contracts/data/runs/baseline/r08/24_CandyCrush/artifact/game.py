if matches:
    cx = sum(config.BOARD_X + c * config.CELL_SIZE + config.CELL_SIZE // 2 for (r, c) in matches) / len(matches)
    cy = sum(config.BOARD_Y + r * config.CELL_SIZE + config.CELL_SIZE // 2 for (r, c) in matches) / len(matches)
    self.floaters.append({"text": f"+{total}", "x": cx, "y": cy, "timer": 1.0, "color": config.ACCENT_COLOR})