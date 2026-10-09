import pygame
import random
import sys

W, H = 480, 640
GRAVITY = 0.45
FLAP_V = -8.0
PIPE_W = 70
GROUND_H = 80
BIRD_X = 90
BIRD_R = 13


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)
    big_font = pygame.font.SysFont(None, 64)
    best = 0

    def new_state():
        return {
            "y": H // 2, "vy": 0.0, "pipes": [], "score": 0,
            "speed": 3.0, "alive": True, "started": False,
        }

    def spawn_pipe(st):
        gap = max(110, 190 - st["score"] * 2) - random.randint(0, 25)
        st["speed"] = min(7.0, 3.0 + st["score"] * 0.1) + random.uniform(0.0, 0.5)
        margin = 50
        top = random.randint(margin, H - GROUND_H - margin - gap)
        st["pipes"].append({"x": W + 10, "top": top, "gap": gap, "passed": False})

    st = new_state()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    if not st["alive"]:
                        st = new_state()
                    elif not st["started"]:
                        st["started"] = True
                        st["vy"] = FLAP_V
                    else:
                        st["vy"] = FLAP_V
                elif event.key == pygame.K_ESCAPE:
                    running = False

        if st["alive"] and st["started"]:
            st["vy"] += GRAVITY
            st["y"] += st["vy"]
            if st["y"] < BIRD_R + 1:
                st["y"] = BIRD_R + 1
                st["vy"] = 0.0

            for p in st["pipes"]:
                p["x"] -= st["speed"]
            st["pipes"] = [p for p in st["pipes"] if p["x"] + PIPE_W > -10]

            spacing = max(190, 280 - st["score"] * 3)
            if not st["pipes"] or st["pipes"][-1]["x"] <= W - spacing:
                spawn_pipe(st)

            bird = pygame.Rect(BIRD_X - BIRD_R + 2, int(st["y"]) - BIRD_R + 2,
                               (BIRD_R - 2) * 2, (BIRD_R - 2) * 2)
            if st["y"] + BIRD_R >= H - GROUND_H:
                st["alive"] = False
                best = max(best, st["score"])
            for p in st["pipes"]:
                top_rect = pygame.Rect(int(p["x"]), 0, PIPE_W, p["top"])
                bot_rect = pygame.Rect(int(p["x"]), p["top"] + p["gap"], PIPE_W,
                                       H - GROUND_H - (p["top"] + p["gap"]))
                if bird.colliderect(top_rect) or bird.colliderect(bot_rect):
                    st["alive"] = False
                    best = max(best, st["score"])
                if not p["passed"] and p["x"] + PIPE_W < bird.left:
                    p["passed"] = True
                    st["score"] += 1

        screen.fill((113, 197, 207))
        for p in st["pipes"]:
            pygame.draw.rect(screen, (56, 160, 70), (int(p["x"]), 0, PIPE_W, p["top"]))
            pygame.draw.rect(screen, (56, 160, 70),
                             (int(p["x"]), p["top"] + p["gap"], PIPE_W,
                              H - GROUND_H - (p["top"] + p["gap"])))
        pygame.draw.rect(screen, (222, 216, 149), (0, H - GROUND_H, W, GROUND_H))
        pygame.draw.rect(screen, (194, 178, 128), (0, H - GROUND_H, W, 12))

        y = int(st["y"])
        pygame.draw.circle(screen, (255, 204, 0), (BIRD_X, y), BIRD_R)
        pygame.draw.circle(screen, (255, 255, 255), (BIRD_X + 5, y - 4), 4)
        pygame.draw.circle(screen, (0, 0, 0), (BIRD_X + 6, y - 4), 2)
        pygame.draw.polygon(screen, (255, 120, 40),
                            [(BIRD_X + BIRD_R, y), (BIRD_X + BIRD_R + 9, y + 3),
                             (BIRD_X + BIRD_R, y + 6)])

        score_surf = big_font.render(str(st["score"]), True, (255, 255, 255))
        screen.blit(score_surf, score_surf.get_rect(center=(W // 2, 60)))

        if not st["started"] and st["alive"]:
            msg = font.render("Press SPACE to flap", True, (255, 255, 255))
            screen.blit(msg, msg.get_rect(center=(W // 2, H // 2 - 80)))
        if not st["alive"]:
            over = big_font.render("Game Over", True, (220, 60, 60))
            info = font.render("Score: %d  Best: %d" % (st["score"], best),
                               True, (255, 255, 255))
            again = font.render("Press SPACE to restart", True, (255, 255, 255))
            screen.blit(over, over.get_rect(center=(W // 2, H // 2 - 60)))
            screen.blit(info, info.get_rect(center=(W // 2, H // 2)))
            screen.blit(again, again.get_rect(center=(W // 2, H // 2 + 50)))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()