"""HUD, menus and overlay screens for the Gold Miner game."""
import pygame
from settings import *
def _bar(surface, x, y, w, h, ratio, fg, bg=(0, 0, 0)):
    pygame.draw.rect(surface, bg, (x, y, w, h))
    pygame.draw.rect(surface, fg, (x, y, int(w * max(0.0, min(1.0, ratio))), h))
    pygame.draw.rect(surface, COLOR_LINE, (x, y, w, h), 2)
def draw_hud(surface, font, big_font, game):
    """Top bar: score vs target progress, level number and timer bar."""
    pygame.draw.rect(surface, COLOR_HUD_BG, (0, 0, SCREEN_WIDTH, SKY_HEIGHT))
    level = game.level
    # Score / target progress bar
    score_text = font.render(f"Gold: {game.level_score} / {level.gold_target}", True, COLOR_YELLOW)
    surface.blit(score_text, (20, 12))
    _bar(surface, 20, 40, 260, 18, game.level_score / level.gold_target, COLOR_GOLD)
    # Timer bar
    time_text = font.render(f"Time: {level.time_left:.1f}s", True, COLOR_WHITE)
    surface.blit(time_text, (320, 12))
    ratio = level.time_left / level.time_limit
    color = COLOR_GREEN if ratio > 0.3 else COLOR_RED
    _bar(surface, 320, 40, 260, 18, ratio, color)
    # Level number
    lvl_text = font.render(f"Level {level.number}", True, COLOR_WHITE)
    surface.blit(lvl_text, (620, 12))
    total_text = font.render(f"Total: {game.total_score}", True, COLOR_WHITE)
    surface.blit(total_text, (620, 40))
def draw_status_panel(surface, font, game):
    """Bottom strip: claw position and objects remaining on the field."""
    claw = game.claw
    tx, ty = claw.tip
    remaining = sum(1 for o in game.level.objects if o.alive)
    line1 = f"Claw angle: {claw.angle:6.1f}°   Length: {claw.length:5.1f}   Tip: ({tx:.0f}, {ty:.0f})   State: {claw.state}"
    line2 = f"Objects left: {remaining}   Last grab: {game.last_grab_text}"
    pygame.draw.rect(surface, COLOR_HUD_BG, (0, SCREEN_HEIGHT - 52, SCREEN_WIDTH, 52))
    t1 = font.render(line1, True, COLOR_WHITE)
    t2 = font.render(line2, True, COLOR_WHITE)
    surface.blit(t1, (16, SCREEN_HEIGHT - 46))
    surface.blit(t2, (16, SCREEN_HEIGHT - 22))
def draw_menu(surface, font, big_font):
    """Title screen with controls."""
    surface.fill(COLOR_SKY_BOTTOM)
    title = big_font.render("GOLD MINER", True, COLOR_GOLD_DARK)
    surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 160)))
    lines = [
        "SPACE / CLICK — launch the claw",
        "Grab gold and gems before time runs out",
        "Reach the gold target to clear each level",
        "Heavy objects reel in slowly — choose wisely!",
        "",
        "Press SPACE or ENTER to start",
    ]
    y = 260
    for line in lines:
        if line:
            txt = font.render(line, True, COLOR_TEXT)
            surface.blit(txt, txt.get_rect(center=(SCREEN_WIDTH // 2, y)))
        y += 34
def draw_level_complete(surface, font, big_font, game):
    """Overlay shown when the gold target is reached."""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))
    t1 = big_font.render(f"Level {game.level_number} Complete!", True, COLOR_GOLD)
    surface.blit(t1, t1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)))
    t2 = font.render(f"Level gold: {game.level_score}    Total score: {game.total_score}", True, COLOR_WHITE)
    surface.blit(t2, t2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
    t3 = font.render("Press SPACE for the next level (faster claw, higher target!)", True, COLOR_WHITE)
    surface.blit(t3, t3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 44)))
def draw_game_over(surface, font, big_font, game):
    """Overlay shown when time runs out before the target is met."""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))
    t1 = big_font.render("Time's Up!", True, COLOR_RED)
    surface.blit(t1, t1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)))
    t2 = font.render(f"You collected {game.level_score} / {game.level.gold_target} gold", True, COLOR_WHITE)
    surface.blit(t2, t2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
    t3 = font.render(f"Final score: {game.total_score}   —   Press SPACE to return to menu", True, COLOR_WHITE)
    surface.blit(t3, t3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 44)))