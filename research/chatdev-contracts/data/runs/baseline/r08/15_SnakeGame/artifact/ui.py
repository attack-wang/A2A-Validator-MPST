def draw_game_over(surface, score, high_score, won, food_count, new_record=False):
    draw_overlay(surface)
    title = "YOU WIN!" if won else "GAME OVER"
    color = config.COLOR_ACCENT if won else config.COLOR_FOOD
    cy = config.WINDOW_HEIGHT // 2
    draw_text(surface, title, 56, color, (config.WINDOW_WIDTH // 2, cy - 90), bold=True)
    draw_text(surface, f"Final Score: {score}", 30, config.COLOR_TEXT, (config.WINDOW_WIDTH // 2, cy - 20))
    draw_text(surface, f"Food Eaten: {food_count}", 24, config.COLOR_TEXT_DIM, (config.WINDOW_WIDTH // 2, cy + 20))
    if new_record:
        draw_text(surface, "NEW HIGH SCORE!", 24, config.COLOR_ACCENT, (config.WINDOW_WIDTH // 2, cy + 55), bold=True)
    else:
        draw_text(surface, f"High Score: {high_score}", 24, config.COLOR_TEXT_DIM, (config.WINDOW_WIDTH // 2, cy + 55))
    draw_text(surface, "R: Restart   M: Menu   ESC: Quit", 20, config.COLOR_TEXT_DIM,
              (config.WINDOW_WIDTH // 2, cy + 110))