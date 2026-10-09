'''
ui.py
Rendering helpers for all user-interface elements: the score bar,
the difficulty-selection menu, the pause overlay, and the game-over
screen.
'''
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_HEIGHT, UI_BAR_HEIGHT,
    CELL_SIZE, GRID_WIDTH, GRID_HEIGHT,
    COLOR_BACKGROUND, COLOR_GRID_LINE, COLOR_UI_BAR,
    COLOR_TEXT, COLOR_TEXT_DIM, COLOR_HIGHLIGHT,
    COLOR_SNAKE_HEAD, COLOR_SNAKE_BODY, COLOR_FOOD,
    DIFFICULTIES,
)
def draw_board(screen):
    """Draw the play-field background and subtle grid lines."""
    board_rect = pygame.Rect(0, UI_BAR_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(screen, COLOR_BACKGROUND, board_rect)
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, COLOR_GRID_LINE,
                         (x, UI_BAR_HEIGHT), (x, WINDOW_HEIGHT))
    for y in range(UI_BAR_HEIGHT, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, COLOR_GRID_LINE,
                         (0, y), (SCREEN_WIDTH, y))
def draw_snake(screen, snake):
    """Draw every snake segment; the head is rendered brighter."""
    offset = UI_BAR_HEIGHT
    for i, (x, y) in enumerate(snake.get_body()):
        color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE_BODY
        rect = pygame.Rect(x * CELL_SIZE, offset + y * CELL_SIZE,
                           CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, color, rect)
        # Small inner border for a cleaner look
        pygame.draw.rect(screen, COLOR_BACKGROUND, rect, 1)
def draw_food(screen, food):
    """Draw the food item as a red square with a rounded look."""
    if food.get_position() is None:
        return
    x, y = food.get_position()
    rect = pygame.Rect(x * CELL_SIZE + 2, UI_BAR_HEIGHT + y * CELL_SIZE + 2,
                       CELL_SIZE - 4, CELL_SIZE - 4)
    pygame.draw.rect(screen, COLOR_FOOD, rect, border_radius=4)
def draw_score_bar(screen, font, score, difficulty_name, high_score=0):
    """Draw the top bar containing score, high score and difficulty."""
    pygame.draw.rect(screen, COLOR_UI_BAR,
                     (0, 0, SCREEN_WIDTH, UI_BAR_HEIGHT))
    score_text = font.render(f"Score: {score}", True, COLOR_TEXT)
    diff_text = font.render(f"Difficulty: {difficulty_name}", True, COLOR_TEXT_DIM)
    high_text = font.render(f"High Score: {high_score}", True, COLOR_HIGHLIGHT)
    screen.blit(score_text, (10, 10))
    screen.blit(diff_text, (SCREEN_WIDTH // 2 - diff_text.get_width() // 2, 10))
    screen.blit(high_text, (SCREEN_WIDTH - high_text.get_width() - 10, 10))
def draw_center_text(screen, big_font, small_font, title, subtitle):
    """Draw a large centered title with a smaller subtitle beneath it."""
    title_surf = big_font.render(title, True, COLOR_HIGHLIGHT)
    sub_surf = small_font.render(subtitle, True, COLOR_TEXT)
    center_x = SCREEN_WIDTH // 2
    center_y = UI_BAR_HEIGHT + SCREEN_HEIGHT // 2
    screen.blit(title_surf, (center_x - title_surf.get_width() // 2,
                             center_y - 60))
    screen.blit(sub_surf, (center_x - sub_surf.get_width() // 2,
                           center_y + 10))
def draw_start_menu(screen, big_font, small_font, selected_index):
    """Draw the difficulty-selection menu with a highlighted option."""
    draw_board(screen)
    title = big_font.render("SNAKE", True, COLOR_HIGHLIGHT)
    center_x = SCREEN_WIDTH // 2
    screen.blit(title, (center_x - title.get_width() // 2, UI_BAR_HEIGHT + 30))
    names = list(DIFFICULTIES.keys())
    y = UI_BAR_HEIGHT + 120
    for i, name in enumerate(names):
        color = COLOR_HIGHLIGHT if i == selected_index else COLOR_TEXT
        prefix = "> " if i == selected_index else "   "
        label = small_font.render(f"{prefix}{name}  "
                                  f"({DIFFICULTIES[name]} moves/sec)",
                                  True, color)
        screen.blit(label, (center_x - label.get_width() // 2, y))
        y += 36
    hint = small_font.render("Up/Down to choose - Enter to start",
                             True, COLOR_TEXT_DIM)
    screen.blit(hint, (center_x - hint.get_width() // 2, WINDOW_HEIGHT - 60))
def draw_pause(screen, big_font, small_font):
    """Draw a semi-transparent pause overlay."""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, UI_BAR_HEIGHT))
    draw_center_text(screen, big_font, small_font,
                     "PAUSED", "Press P to resume")
def draw_game_over(screen, big_font, small_font, score, won):
    """Draw the game-over overlay with the final score."""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, UI_BAR_HEIGHT))
    title = "YOU WIN!" if won else "GAME OVER"
    subtitle = f"Final Score: {score}  -  Enter: menu, Esc: quit"
    draw_center_text(screen, big_font, small_font, title, subtitle)