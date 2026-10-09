class MysteryBag(GameObject):
    def __init__(self, x, y):
        super().__init__("mystery_bag", x, y)
    def on_grab(self, game):
        # resolve random content when grabbed
        roll = random.random()
        if roll < 0.45:
            self.value = random.choice([100, 200, 350])
            game.on_bag_reveal(self, "Gold!")
        elif roll < 0.65:
            self.value = 500
            game.on_bag_reveal(self, "Jackpot!")
        elif roll < 0.85:
            self.value = random.choice([-50, -100])
            game.on_bag_reveal(self, "Trap!")
        else:
            self.value = 0
            game.on_bag_reveal(self, "Empty...")
    def draw(self, surface):
        r = self.radius
        # sack shape
        pts = [
            (self.x - r, self.y + r * 0.9),
            (self.x - r * 0.9, self.y - r * 0.2),
            (self.x - r * 0.4, self.y - r * 1.0),
            (self.x + r * 0.4, self.y - r * 1.0),
            (self.x + r * 0.9, self.y - r * 0.2),
            (self.x + r, self.y + r * 0.9),
        ]
        pygame.draw.polygon(surface, config.COLOR_BAG, pts)
        pygame.draw.polygon(surface, (110, 70, 40), pts, 2)
        # tied top
        pygame.draw.line(surface, (110, 70, 40), (self.x - r*0.4, self.y - r*1.0), (self.x + r*0.4, self.y - r*1.0), 3)
        # question mark
        font = _small_font()
        label = font.render("?", True, (240, 230, 200))
        surface.blit(label, (self.x - label.get_width()//2, self.y - label.get_height()//2))