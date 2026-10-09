import sys
import pygame

from game import Game2048

CELL = 100
GAP = 10
PADDING = 10
HEADER = 70
WIDTH = PADDING * 2 + CELL * 4 + GAP * 3
HEIGHT = HEADER + PADDING * 2 + CELL * 4 + GAP * 3

BG = (187, 173, 160)
EMPTY = (205, 193, 180)
TEXT = (119, 110, 101)
LIGHT = (249, 246, 242)

TILE_COLORS = {
    2: (238, 228, 218), 4: (237, 224, 200), 8: (242, 177, 121),
    16: (245, 149, 99), 32: (246, 124, 95), 64: (246, 94, 59),
    128: (237, 207, 114), 256: (237, 204, 97), 512: (237, 200, 80),
    1024: (237, 197, 63), 2048: (237, 194, 46),
}

FONTS = {}


def get_font(size):
    if size not in FONTS:
        FONTS[size] = pygame.font.SysFont("arial", size, bold=True)
    return FONTS[size]


def tile_color(value):
    return TILE_COLORS.get(value, (60, 58, 50))


def draw(screen, game):
    screen.fill(BG)
    score_s = get_font(24).render("Score: %d" % game.score, True, TEXT)
    high_s = get_font(24).render("Highest tile: %d" % game.highest, True, TEXT)
    screen.blit(score_s, (PADDING, 18))
    screen.blit(high_s, (WIDTH - high_s.get_width() - PADDING, 18))
    if game.won and not game.over:
        win_s = get_font(20).render("2048 reached! Keep going...", True, TEXT)
        screen.blit(win_s, ((WIDTH - win_s.get_width()) // 2, 44))
    for r in range(4):
        for c in range(4):
            x = PADDING + c * (CELL + GAP)
            y = HEADER + PADDING + r * (CELL + GAP)
            rect = pygame.Rect(x, y, CELL, CELL)
            value = game.board[r][c]
            color = EMPTY if value == 0 else tile_color(value)
            pygame.draw.rect(screen, color, rect, border_radius=6)
            if value:
                fg = TEXT if value <= 4 else LIGHT
                size = 48 if value < 100 else 40 if value < 1000 else 30
                s = get_font(size).render(str(value), True, fg)
                screen.blit(s, s.get_rect(center=rect.center))
    if game.over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((238, 228, 218, 160))
        screen.blit(overlay, (0, 0))
        msg = get_font(48).render("Game Over!", True, TEXT)
        screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        hint = get_font(24).render("Press R to restart", True, TEXT)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))
    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048")
    game = Game2048()
    clock = pygame.time.Clock()
    keys = {
        pygame.K_LEFT: "left",
        pygame.K_RIGHT: "right",
        pygame.K_UP: "up",
        pygame.K_DOWN: "down",
    }
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                elif event.key in keys:
                    game.move(keys[event.key])
        draw(screen, game)
        clock.tick(60)


if __name__ == "__main__":
    main()