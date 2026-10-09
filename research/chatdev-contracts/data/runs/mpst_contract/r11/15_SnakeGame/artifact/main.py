import pygame

from game import Game
from settings import WIDTH, HEIGHT, DIFFICULTIES, COLORS


def choose_difficulty(screen):
    font = pygame.font.SysFont(None, 40)
    while True:
        screen.fill(COLORS["bg"])
        title = font.render("Select Difficulty", True, COLORS["text"])
        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 90)))
        items = list(DIFFICULTIES.items())
        for i, (key, (name, speed)) in enumerate(items):
            line = font.render(f"[{key}] {name}", True, COLORS["text"])
            screen.blit(line, line.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 45)))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN and pygame.K_1 <= event.key <= pygame.K_3:
                return DIFFICULTIES[str(event.key - pygame.K_0)][1]


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    while True:
        speed = choose_difficulty(screen)
        if speed is None:
            break
        if Game(screen, speed).run():
            break
    pygame.quit()


if __name__ == "__main__":
    main()