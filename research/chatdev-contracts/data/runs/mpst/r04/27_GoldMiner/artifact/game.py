def draw(self, surface):
    # rope
    pygame.draw.line(surface, COLOR_ROPE, self.pivot, self.tip, 3)
    # pulley
    pygame.draw.circle(surface, COLOR_CLAW, self.pivot, 10)
    pygame.draw.circle(surface, COLOR_BLACK, self.pivot, 10, 2)
    # claw head
    tip = self.tip
    pygame.draw.circle(surface, COLOR_CLAW, tip, 8)
    # prongs
    rad = math.radians(self.angle)
    # perpendicular direction
    px, py = math.cos(rad), -math.sin(rad)
    open_amount = 12 if self.grabbed is None else 6
    for side in (-1, 1):
        bx = tip[0] + px * side * open_amount
        by = tip[1] + py * side * open_amount
        # prong tip extends downward beyond the head
        ex = tip[0] + math.sin(rad) * 16 + px * side * (open_amount - 6)
        ey = tip[1] + math.cos(rad) * 16 + py * side * (open_amount - 6)
        pygame.draw.line(surface, COLOR_CLAW, (bx, by), (ex, ey), 4)