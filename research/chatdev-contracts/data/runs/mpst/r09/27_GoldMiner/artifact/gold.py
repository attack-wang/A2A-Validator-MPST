class Gold(GameObject):
    """A gold nugget. Bigger nuggets are worth more but reel in slowly."""
    def __init__(self, x, y, size="small"):
        spec = {"small": config.GOLD_SMALL,
                "medium": config.GOLD_MEDIUM,
                "large": config.GOLD_LARGE}[size]
        super().__init__(x, y, spec["name"], spec["value"], spec["weight"],
                         spec["radius"], config.COLOR_GOLD, "gold")
        self.size = size
    def draw(self, surface):
        r = self.radius
        cx, cy = int(self.x), int(self.y)
        # irregular nugget polygon
        pts = []
        for i in range(8):
            ang = math.radians(i * 45 + 22)
            jitter = r * (0.75 + 0.25 * ((i * 37) % 7) / 6.0)
            pts.append((cx + math.cos(ang) * jitter, cy + math.sin(ang) * jitter))
        pygame.draw.polygon(surface, self.color, pts)
        pygame.draw.polygon(surface, config.COLOR_GOLD_DARK, pts, 2)
        # shine
        pygame.draw.circle(surface, (255, 245, 180),
                           (cx - r // 3, cy - r // 3), max(2, r // 4))