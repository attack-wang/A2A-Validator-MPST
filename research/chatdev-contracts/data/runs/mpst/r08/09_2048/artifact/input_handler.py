import pygame
DIRECTION_MAP = {
    pygame.K_UP: 'up',
    pygame.K_DOWN: 'down',
    pygame.K_LEFT: 'left',
    pygame.K_RIGHT: 'right',
    pygame.K_w: 'up',
    pygame.K_s: 'down',
    pygame.K_a: 'left',
    pygame.K_d: 'right',
}
def get_move_direction(events):
    for event in events:
        if event.type == pygame.KEYDOWN:
            direction = DIRECTION_MAP.get(event.key)
            if direction:
                return direction
    return None