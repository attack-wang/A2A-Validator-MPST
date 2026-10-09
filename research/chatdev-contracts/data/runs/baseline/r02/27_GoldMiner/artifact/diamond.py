class Diamond(GameObject):
    '''Rare, light and extremely valuable.'''
    def draw(self, surface):
        x, y = int(self.x), int(self.y)
        r = self.radius
        points = [(x, y - r), (x + r, y), (x, y + r), (x - r, y)]
        pygame.draw.polygon(surface, DIAMOND_COLOR, points)
        pygame.draw.polygon(surface, DIAMOND_DARK, points, 2)
        pygame.draw.line(surface, WHITE, (x, y - r), (x, y + r), 1)
        # twinkle
        tw = (math.sin(self.wobble) + 1) / 2
        ...