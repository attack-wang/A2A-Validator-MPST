import pygame
import random
import sys

WIDTH, HEIGHT = 480, 640
GROUND_H = 80
PIPE_W = 60
BIRD_X = 80
FPS = 60

SKY = (113, 197, 207)
GROUND = (222, 216, 149)
GROUND_TOP = (200, 190, 120)
GREEN = (76, 175, 80)
DARK = (40, 40, 40)
YELLOW = (255, 210, 60)
ORANGE = (255, 140, 0)
WHITE = (255, 255, 255)


def new_state():
    return {
        "bird_y": HEIGHT // 2, "vel": 0.0, "pipes": [], "score": 0,
        "spawn_timer": 0, "alive": True, "started": False, "dead_timer": 0,
    }


def difficulty(score):
    speed = min(3.0 + score * 0.05, 6.0)
    base_gap = max(220 - score * 4, 120)
    return speed, base_gap


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()
    font_big = pygame.font.Font(None, 56)
    font = pygame.font.Font(None, 32)
    font_small = pygame.font.Font(None, 24)

    state = new_state()
    best = 0

    def bird_rect():
        return pygame.Rect(BIRD_X, int(state["bird_y"]) - 15, 30, 30)

    def spawn_pipe():
        speed, base_gap = difficulty(state["score"])
        gap = max(110, min(260, base_gap + random.randint(-20, 20)))
        lo = gap // 2 + 40
        hi = HEIGHT - GROUND_H - gap // 2 - 40
        gap_y = random.randint(lo, hi)
        state["pipes"].append(
            {"x": WIDTH, "gap_y": gap_y, "gap": gap, "speed": speed, "passed": False}
        )

    def flap():
        if not state["alive"]:
            if state["dead_timer"] > 30:
                state.clear()
                state.update(new_state())
        elif not state["started"]:
            state["started"] = True
            state["vel"] = -8.0
        else:
            state["vel"] = -8.0

    def collide():
        r = bird_rect()
        if r.bottom >= HEIGHT - GROUND_H:
            return True
        for p in state["pipes"]:
            top_h = p["gap_y"] - p["gap"] // 2
            bot_y = p["gap_y"] + p["gap"] // 2
            if r.right > p["x"] and r.left < p["x"] + PIPE_W:
                if r.top < top_h or r.bottom > bot_y:
                    return True
        return False

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_SPACE, pygame.K_UP):
                    flap()
                elif e.key == pygame.K_ESCAPE:
                    running = False

        if state["alive"] and state["started"]:
            state["vel"] = min(state["vel"] + 0.35, 10.0)
            state["bird_y"] += state["vel"]
            if state["bird_y"] < 15:
                state["bird_y"] = 15
                state["vel"] = 0.0
            state["spawn_timer"] -= 1
            if state["spawn_timer"] <= 0:
                spawn_pipe()
                speed, _ = difficulty(state["score"])
                state["spawn_timer"] = max(40, int(260 / speed))
            for p in state["pipes"]:
                p["x"] -= p["speed"]
                if not p["passed"] and p["x"] + PIPE_W < BIRD_X:
                    p["passed"] = True
                    state["score"] += 1
            state["pipes"] = [p for p in state["pipes"] if p["x"] > -PIPE_W - 10]
            if collide():
                state["alive"] = False
                best = max(best, state["score"])
        elif not state["alive"]:
            state["dead_timer"] += 1

        screen.fill(SKY)
        for p in state["pipes"]:
            top_h = p["gap_y"] - p["gap"] // 2
            bot_y = p["gap_y"] + p["gap"] // 2
            pygame.draw.rect(screen, GREEN, (p["x"], 0, PIPE_W, top_h))
            pygame.draw.rect(screen, GREEN, (p["x"], bot_y, PIPE_W, HEIGHT - GROUND_H - bot_y))
            pygame.draw.rect(screen, DARK, (p["x"], 0, PIPE_W, top_h), 2)
            pygame.draw.rect(screen, DARK, (p["x"], bot_y, PIPE_W, HEIGHT - GROUND_H - bot_y), 2)
        pygame.draw.rect(screen, GROUND, (0, HEIGHT - GROUND_H, WIDTH, GROUND_H))
        pygame.draw.rect(screen, GROUND_TOP, (0, HEIGHT - GROUND_H, WIDTH, 10))

        r = bird_rect()
        pygame.draw.ellipse(screen, YELLOW, r)
        pygame.draw.rect(screen, DARK, r, 2)
        pygame.draw.circle(screen, DARK, (r.right - 8, r.top + 10), 3)
        pygame.draw.polygon(screen, ORANGE, [
            (r.right - 2, r.centery), (r.right + 9, r.centery + 2), (r.right - 2, r.centery + 6)
        ])
        wing_y = r.centery - 4 + (4 if state["vel"] > 0 else -4)
        pygame.draw.ellipse(screen, ORANGE, (r.left + 2, wing_y, 13, 8))

        score_surf = font_big.render(str(state["score"]), True, WHITE)
        screen.blit(score_surf, score_surf.get_rect(center=(WIDTH // 2, 60)))
        speed, gap = difficulty(state["score"])
        info = font_small.render(f"speed {speed:.1f}   gap ~{gap}", True, WHITE)
        screen.blit(info, (10, 10))

        if state["alive"] and not state["started"]:
            t1 = font.render("Press SPACE to flap", True, WHITE)
            t2 = font.render("Avoid the pipes and the ground", True, WHITE)
            screen.blit(t1, t1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
            screen.blit(t2, t2.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        elif not state["alive"]:
            t1 = font_big.render("Game Over", True, ORANGE)
            t2 = font.render(f"Score: {state['score']}   Best: {best}", True, WHITE)
            t3 = font.render("Press SPACE to restart", True, WHITE)
            screen.blit(t1, t1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60)))
            screen.blit(t2, t2.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            screen.blit(t3, t3.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()