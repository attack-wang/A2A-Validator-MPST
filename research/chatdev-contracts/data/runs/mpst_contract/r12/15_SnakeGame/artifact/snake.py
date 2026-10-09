from settings import COLS, ROWS


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        cx, cy = COLS // 2, ROWS // 2
        self.body = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = (1, 0)
        self.prev_direction = self.direction
        self.grow_pending = 0

    def set_direction(self, direction):
        # Validate against the direction actually used in the last executed
        # step, so multiple keypresses within one tick can never produce a
        # 180-degree turn and an unfair instant self-collision.
        if direction[0] == -self.prev_direction[0] and direction[1] == -self.prev_direction[1]:
            return
        self.direction = direction

    def step(self):
        self.prev_direction = self.direction
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        self.body.insert(0, (head_x + dx, head_y + dy))
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def hits_wall(self):
        x, y = self.body[0]
        return x < 0 or y < 0 or x >= COLS or y >= ROWS

    def hits_self(self):
        return self.body[0] in self.body[1:]