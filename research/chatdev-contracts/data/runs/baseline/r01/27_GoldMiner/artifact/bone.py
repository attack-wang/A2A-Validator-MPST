class Bone(GameObject):
    """Leftover scrap; tiny value, light weight."""
    def __init__(self, x, y):
        super().__init__(x, y, 12, 15, 1.5, 'bone')
    def draw(self, surface):
        x, y = int(self.x), int(self.y)
        pygame.draw.line(surface, BONE_COLOR, (x - 8, y + 5), (x + 8, y - 5), 5)
        pygame.draw.circle(surface, BONE_COLOR, (x - 9, y + 7), 4)
        pygame.draw.circle(surface, BONE_COLOR, (x - 6, y + 10), 4)
        pygame.draw.circle(surface, BONE_COLOR, (x + 9, y - 7), 4)
        pygame.draw.circle(surface, BONE_COLOR, (x + 6, y - 10), 4)