class Rock(GameObject):
    '''A worthless-ish heavy rock; still worth a few points.'''
    def draw(self, surface):
        x, y = int(self.x), int(self.y)
        r = self.radius
        points = []
        n = 7
        for i in range(n):
            ang = math.tau * i / n + self.wobble
            rr = r * (0.85 + 0.15 * math.sin(self.wobble * 3 + i * 1.7))
            points.append((x + math.cos(ang) * rr, y + math.sin(ang) * rr))
        pygame.draw.polygon(surface, ROCK_COLOR, points)
        pygame.draw.polygon(surface, ROCK_DARK, points, 2)
        pygame.draw.circle(surface, ROCK_DARK, (x + r // 4, y - r // 5), max(2, r // 6))