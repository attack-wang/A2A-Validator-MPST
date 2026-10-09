'''
ui.py
Rendering and screen-flow helpers for the Snake game.
Contains:
  * drawing routines for the board, snake, food, score HUD,
    and the pause overlay,
  * the main menu (difficulty selection) screen,
  * the game-over / victory screen.
All screens return a control value so main.py can orchestrate
the application flow.
'''
import pygame
import settings
# ----------------------------------------------------------------------
# Low-level drawing helpers
# ----------------------------------------------------------------------
def grid_to_rect(x, y):
    """Convert grid coordinates to a pixel Rect on the board."""
    return pygame.Rect(
        x * settings.GRID_SIZE,
        settings.BOARD_OFFSET_Y + y * settings.GRID_SIZE,
        settings.GRID_SIZE,
        settings.GRID_SIZE,
    )
def draw_board(surface):
    """Draw the HUD background, checkerboard playfield, and border."""
    hud_rect = pygame.Rect(0, 0, settings.WINDOW_WIDTH, settings.HUD_HEIGHT)
    pygame.draw.rect(surface, settings.HUD_COLOR, hud_rect)
    for x in range(settings.GRID_WIDTH):
        for y in range(settings.GRID_HEIGHT):
            color = settings.BOARD_COLOR_A if (x + y) % 2 == 0 else settings.BOARD_COLOR_B
            pygame.draw.rect(surface, color, grid_to_rect(x, y))
    board_rect = pygame.Rect(
        0,
        settings.BOARD_OFFSET_Y,
        settings.BOARD_WIDTH,
        settings.BOARD_HEIGHT,
    )
    pygame.draw.rect(surface, settings.SNAKE_BODY_COLOR, board_rect, 2)
def draw_snake(surface, snake):
    """Draw every snake segment; the head is brighter, the body alternates shades."""
    for i, (x, y) in enumerate(snake.get_body()):
        if i == 0:
            color = settings.SNAKE_HEAD_COLOR
        elif i % 2 == 1:
            color = settings.SNAKE_BODY_COLOR
        else:
            color = settings.SNAKE_BODY_ALT_COLOR
        rect = grid_to_rect(x, y).inflate(-2, -2)  # small gap between segments
        pygame.draw.rect(surface, color, rect, border_radius=4)
def draw_food(surface, food):
    """Draw the food as a shaded circle at its grid position."""
    if food.position is None:
        return
    rect = grid_to_rect(*food.position)
    center = rect.center
    radius = settings.GRID_SIZE // 2 - 3
    pygame.draw.circle(surface, settings.FOOD_COLOR, center, radius)
    # Small highlight for a glossy look
    highlight_center = (center[0] - radius // 3, center[1] - radius // 3)
    pygame.draw.circle(
        surface, settings.FOOD_HIGHLIGHT_COLOR, highlight_center, max(2, radius // 3)
    )
def draw_hud(surface, score, difficulty, length):
    """Draw the top bar with the current score and session info."""
    font = pygame.font.Font(settings.FONT_NAME, settings.FONT_SIZE_SCORE)
    small_font = pygame.font.Font(settings.FONT_NAME, settings.FONT_SIZE_SMALL)
    score_text = font.render(f"Score: {score}", True, settings.SCORE_COLOR)
    surface.blit(score_text, (10, 8))
    diff_text = small_font.render(f"Difficulty: {difficulty}", True, settings.TEXT_COLOR)
    surface.blit(diff_text, (170, 12))
    length_text = small_font.render(f"Length: {length}", True, settings.TEXT_COLOR)
    surface.blit(length_text, (settings.WINDOW_WIDTH - 130, 12))
def render_game(surface, game):
    """Compose one full frame of an ongoing game session."""
    surface.fill(settings.BLACK)
    draw_board(surface)
    draw_food(surface, game.food)
    draw_snake(surface, game.snake)
    draw_hud(surface, game.score, game.difficulty_name, game.snake.get_length())
def draw_pause_overlay(surface):
    """Dim the board and show a PAUSED message (toggled with P)."""
    overlay = pygame.Surface(
        (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), pygame.SRCALPHA
    )
    overlay.fill(settings.OVERLAY_COLOR)
    surface.blit(overlay, (0, 0))
    title_font = pygame.font.Font(settings.FONT_NAME, settings.FONT_SIZE_TITLE)
    small_font = pygame.font.Font(settings.FONT_NAME, settings.FONT_SIZE_SMALL)
    title = title_font.render("PAUSED", True, settings.TEXT_COLOR)
    surface.blit(
        title, title.get_rect(center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2 - 20))
    )
    hint = small_font.render("Press P to resume", True, settings.MENU_NORMAL_COLOR)
    surface.blit(
        hint, hint.get_rect(center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2 + 30))
    )
# ----------------------------------------------------------------------
# Screen flow
# ----------------------------------------------------------------------
def show_menu(screen, clock):
    """
    Display the difficulty-selection menu.
    Up/Down (or W/S) move the selection, Enter/Space confirm,
    Esc or the window close button exits the application.
    Returns the chosen difficulty name, or None to quit.
    """
    options = list(settings.DIFFICULTY_SETTINGS.keys())
    selected = options.index("Medium") if "Medium" in options else 0
    title_font = pygame.font.Font(settings.FONT_NAME, settings.FONT_SIZE_TITLE)
    menu_font = pygame.font.Font(settings.FONT_NAME, settings.FONT_SIZE_MENU)
    small_font = pygame.font.Font(settings.FONT_NAME, settings.FONT_SIZE_SMALL)
    while True:
        clock.tick(settings.BASE_FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(options)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return options[selected]
                elif event.key == pygame.K_ESCAPE:
                    return None
        screen.fill(settings.BLACK)
        title = title_font.render("SNAKE", True, settings.MENU_TITLE_COLOR)
        screen.blit(title, title.get_rect(center=(settings.WINDOW_WIDTH // 2, 80)))
        subtitle = small_font.render(
            "Select difficulty (Up/Down + Enter)", True, settings.MENU_NORMAL_COLOR
        )
        screen.blit(subtitle, subtitle.get_rect(center=(settings.WINDOW_WIDTH // 2, 130)))
        for i, name in enumerate(options):
            color = settings.MENU_SELECTED_COLOR if i == selected else settings.MENU_NORMAL_COLOR
            prefix = "> " if i == selected else "  "
            text = menu_font.render(prefix + name, True, color)
            screen.blit(text, (settings.WINDOW_WIDTH // 2 - 110, 175 + i * 45))
            desc = small_font.render(
                settings.DIFFICULTY_SETTINGS[name]["description"],
                True,
                settings.MENU_NORMAL_COLOR,
            )
            screen.blit(desc, (settings.WINDOW_WIDTH // 2 - 110, 200 + i * 45))
        pygame.display.flip()
def show_game_over(screen, clock, score, victory=False):
    """
    Game-over / victory screen shown on top of the last board frame.
    Up/Down (or W/S) + Enter choose an option; Esc returns to the menu.
    Returns 'restart', 'menu', or 'quit'.
    """
    overlay = pygame.Surface(
        (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), pygame.SRCALPHA
    )
    overlay.fill(settings.OVERLAY_COLOR)
    title_font = pygame.font.Font(settings.FONT_NAME, settings.FONT_SIZE_TITLE)
    menu_font = pygame.font.Font(settings.FONT_NAME, settings.FONT_SIZE_MENU)
    options = ["Play Again", "Main Menu", "Quit"]
    selected = 0
    while True:
        clock.tick(settings.BASE_FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(options)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return ["restart", "menu", "quit"][selected]
                elif event.key == pygame.K_ESCAPE:
                    return "menu"
        # The last rendered game frame is still on the display surface;
        # dim it with the overlay and draw the results on top.
        screen.blit(overlay, (0, 0))
        title_text = "VICTORY!" if victory else "GAME OVER"
        title_color = settings.MENU_TITLE_COLOR if victory else settings.FOOD_COLOR
        title = title_font.render(title_text, True, title_color)
        screen.blit(title, title.get_rect(center=(settings.WINDOW_WIDTH // 2, 130)))
        score_surf = menu_font.render(f"Final Score: {score}", True, settings.SCORE_COLOR)
        screen.blit(score_surf, score_surf.get_rect(center=(settings.WINDOW_WIDTH // 2, 190)))
        for i, name in enumerate(options):
            color = settings.MENU_SELECTED_COLOR if i == selected else settings.MENU_NORMAL_COLOR
            prefix = "> " if i == selected else "  "
            text = menu_font.render(prefix + name, True, color)
            screen.blit(text, text.get_rect(center=(settings.WINDOW_WIDTH // 2, 250 + i * 40)))
        pygame.display.flip()