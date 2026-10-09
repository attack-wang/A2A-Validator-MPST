import math
import random
import sys

import pygame

W, H = 400, 600
GROUND_H = 80
FPS = 60
GRAVITY = 0.45
FLAP_V = -7.5
PIPE_W = 60
PIPE_SPACING = 210
BIRD_X = 100
BIRD_R = 12

SKY = (113, 197, 207)
GREEN = (111, 196, 69)
DARK = (56, 112, 38)
YELLOW = (255, 204, 0)
ORANGE = (255, 140, 0)
BROWN = (222, 184, 135)
WHITE = (255, 255, 255)

pygame.init()
SCREEN = pygame.display.set_mode((W, H))
pygame.display.set_caption("Flappy Bird")
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("arial", 30, bold=True)
SMALL = pygame.font.SysFont("arial", 18)


def current_speed(score):
    return min(6.0, 2.5 + score * 0.08)


def spawn_pipe(pipes, x, score):
    gap = max(105, 170 - score * 3 + random.randint(-10, 10))
    margin = 50
    lo = margin + gap / 2
    hi = H - GROUND_H - margin - gap / 2
    center = random.uniform(lo, hi)
    pipes.append({"x": x, "center": center, "gap": gap, "scored": False})


def reset_game():
    return {"bird_y": H * 0.4, "vel": 0.0, "pipes": [], "score": 0,
            "dist": PIPE_SPACING, "alive": True, "started": False}


def flap(state):
    state["vel"] = FLAP_V


def update(state):
    if not state["started"] or not state["alive"]:
        if not state["started"]:
            state["bird_y"] = H * 0.4 + math.sin(pygame.time.get_ticks() * 0.005) * 8
        return
    state["vel"] += GRAVITY
    state["bird_y"] += state["vel"]
    if state["bird_y"] < BIRD_R:
        state["bird_y"] = BIRD_R
        state["vel"] = 0

    speed = current_speed(state["score"])
    state["dist"] += speed
    if state["dist"] >= PIPE_SPACING:
        state["dist"] = 0
        spawn_pipe(state["pipes"], W + PIPE_W, state["score"])

    bird = pygame.Rect(BIRD_X - BIRD_R, state["bird_y"] - BIRD_R, BIRD_R * 2, BIRD_R * 2)
    for p in state["pipes"]:
        p["x"] -= speed
        top_h = p["center"] - p["gap"] / 2
        bot_y = p["center"] + p["gap"] / 2
        top = pygame.Rect(p["x"], 0, PIPE_W, top_h)
        bot = pygame.Rect(p["x"], bot_y, PIPE_W, H - GROUND_H - bot_y)
        if bird.colliderect(top) or bird.colliderect(bot):
            state["alive"] = False
        if not p["scored"] and p["x"] + PIPE_W < BIRD_X - BIRD_R:
            p["scored"] = True
            state["score"] += 1
    state["pipes"] = [p for p in state["pipes"] if p["x"] + PIPE_W > -10]

    if state["bird_y"] + BIRD_R >= H - GROUND_H:
        state["bird_y"] = H - GROUND_H - BIRD_R
        state["alive"] = False


def draw(state):
    SCREEN.fill(SKY)
    for p in state["pipes"]:
        top_h = int(p["center"] - p["gap"] / 2)
        bot_y = int(p["center"] + p["gap"] / 2)
        pygame.draw.rect(SCREEN, GREEN, (p["x"] - 4, top_h - 20, PIPE_W + 8, 20))
        pygame.draw.rect(SCREEN, GREEN, (p["x"] - 4, bot_y, PIPE_W + 8, 20))
        pygame.draw.rect(SCREEN, GREEN, (p["x"], 0, PIPE_W, top_h))
        pygame.draw.rect(SCREEN, GREEN, (p["x"], bot_y, PIPE_W, H - GROUND_H - bot_y))
        pygame.draw.rect(SCREEN, DARK, (p["x"], 0, PIPE_W, top_h), 2)
        pygame.draw.rect(SCREEN, DARK, (p["x"], bot_y, PIPE_W, H - GROUND_H - bot_y), 2)
    pygame.draw.rect(SCREEN, BROWN, (0, H - GROUND_H, W, GROUND_H))
    pygame.draw.rect(SCREEN, DARK, (0, H - GROUND_H, W, 6))
    by = int(state["bird_y"])
    pygame.draw.circle(SCREEN, YELLOW, (BIRD_X, by), BIRD_R)
    pygame.draw.ellipse(SCREEN, ORANGE, (BIRD_X - 9, by - 2, 11, 8))
    pygame.draw.circle(SCREEN, ORANGE, (BIRD_X + 10, by + 2), 4)
    pygame.draw.circle(SCREEN, (0, 0, 0), (BIRD_X + 4, by - 4), 2)
    surf = FONT.render(str(state["score"]), True, WHITE)
    SCREEN.blit(surf, (W // 2 - surf.get_width() // 2, 20))
    if not state["started"]:
        msg = SMALL.render("Press SPACE to flap!", True, WHITE)
        SCREEN.blit(msg, (W // 2 - msg.get_width() // 2, H // 2 - 40))
    if not state["alive"]:
        over = FONT.render("Game Over", True, WHITE)
        SCREEN.blit(over, (W // 2 - over.get_width() // 2, H // 2 - 60))
        msg = SMALL.render("Score: %d  -  Press SPACE to restart" % state["score"], True, WHITE)
        SCREEN.blit(msg, (W // 2 - msg.get_width() // 2, H // 2 - 10))
    pygame.display.flip()


def main():
    state = reset_game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    if not state["alive"]:
                        state = reset_game()
                    elif not state["started"]:
                        state["started"] = True
                        flap(state)
                    else:
                        flap(state)
                elif event.key == pygame.K_ESCAPE:
                    running = False
        update(state)
        draw(state)
        CLOCK.tick(FPS)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()