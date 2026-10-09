import pygame, random, sys

W, H, GROUND = 480, 640, 560
PIPE_W = 52

def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Flappy Bird Clone")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)
    big = pygame.font.SysFont(None, 72)
    state = {}

    def reset():
        state.update(bird_y=H / 2.0, bird_v=0.0, pipes=[], score=0,
                     speed=3.0, gap=170, alive=True, started=False, frames=0)

    reset()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_SPACE, pygame.K_UP):
                    if state["alive"]:
                        state["started"] = True
                        state["bird_v"] = -8.5
                    else:
                        reset()
                elif e.key == pygame.K_ESCAPE:
                    running = False

        s = state
        if s["alive"] and s["started"]:
            s["frames"] += 1
            if s["frames"] % 600 == 0:  # ramp difficulty every ~10 seconds
                s["speed"] = min(s["speed"] + 0.4, 7.0)
                s["gap"] = max(s["gap"] - 8, 120)
            s["bird_v"] = min(s["bird_v"] + 0.45, 12.0)
            s["bird_y"] += s["bird_v"]
            if s["bird_y"] < 0:
                s["bird_y"] = 0
                s["bird_v"] = 0
            if not s["pipes"] or s["pipes"][-1]["x"] < W - 230:
                g = max(100, s["gap"] + random.randint(-15, 15))
                top = random.randint(60, GROUND - g - 60)
                s["pipes"].append({"x": W + 40, "top": top, "gap": g, "scored": False})
            bird = pygame.Rect(80, int(s["bird_y"]) - 12, 24, 24)
            if bird.bottom >= GROUND:
                s["alive"] = False
            for p in s["pipes"]:
                p["x"] -= s["speed"]
                if not p["scored"] and p["x"] + PIPE_W < 80:
                    p["scored"] = True
                    s["score"] += 1
                top_rect = pygame.Rect(int(p["x"]), 0, PIPE_W, p["top"])
                bot_rect = pygame.Rect(int(p["x"]), p["top"] + p["gap"],
                                       PIPE_W, GROUND - p["top"] - p["gap"])
                if bird.colliderect(top_rect) or bird.colliderect(bot_rect):
                    s["alive"] = False
            s["pipes"] = [p for p in s["pipes"] if p["x"] > -PIPE_W]

        screen.fill((113, 197, 207))
        for p in s["pipes"]:
            x = int(p["x"])
            pygame.draw.rect(screen, (76, 175, 80), (x, 0, PIPE_W, p["top"]))
            pygame.draw.rect(screen, (76, 175, 80),
                             (x, p["top"] + p["gap"], PIPE_W, GROUND - p["top"] - p["gap"]))
        pygame.draw.rect(screen, (222, 184, 135), (0, GROUND, W, H - GROUND))
        pygame.draw.rect(screen, (160, 120, 70), (0, GROUND, W, 8))
        pygame.draw.circle(screen, (255, 215, 0), (92, int(s["bird_y"])), 12)
        pygame.draw.circle(screen, (0, 0, 0), (98, int(s["bird_y"]) - 4), 3)
        txt = font.render(str(s["score"]), True, (255, 255, 255))
        screen.blit(txt, (W // 2 - txt.get_width() // 2, 20))
        if s["alive"] and not s["started"]:
            t = font.render("Press SPACE to flap", True, (255, 255, 255))
            screen.blit(t, (W // 2 - t.get_width() // 2, H // 2 - 60))
        if not s["alive"]:
            t1 = big.render("GAME OVER", True, (200, 30, 30))
            t2 = font.render("Score: %d  -  SPACE to retry" % s["score"], True, (255, 255, 255))
            screen.blit(t1, (W // 2 - t1.get_width() // 2, H // 2 - 80))
            screen.blit(t2, (W // 2 - t2.get_width() // 2, H // 2 + 10))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()