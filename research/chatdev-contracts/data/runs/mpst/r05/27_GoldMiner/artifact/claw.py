    def draw(self, surface):
        # rope
        pygame.draw.line(surface, COLOR_LINE, self.pivot, self.tip, 3)
        # claw jaws at the tip, oriented along the rope
        rad = math.radians(self.angle)
        tx, ty = self.tip
        dir_x, dir_y = math.sin(rad), math.cos(rad)
        perp_x, perp_y = -dir_y, dir_x
        open_w = self.claw_size
        left = (tx - perp_x * open_w - dir_x * 4, ty - perp_y * open_w - dir_y * 4)
        right = (tx + perp_x * open_w - dir_x * 4, ty + perp_y * open_w - dir_y * 4)
        pygame.draw.line(surface, COLOR_LINE, (tx, ty), left, 4)
        pygame.draw.line(surface, COLOR_LINE, (tx, ty), right, 4)
        # pivot wheel
        pygame.draw.circle(surface, COLOR_LINE, self.pivot, 10)
        pygame.draw.circle(surface, COLOR_GOLD, self.pivot, 6)