class Bone(GameObject):
    """A buried bone: light to reel in but nearly worthless."""
    def __init__(self, x, y):
        super().__init__(x, y, 'bone', S.BONE_VALUE, S.BONE_WEIGHT, S.BONE_RADIUS)
        self.angle = random.uniform(0, math.pi)
    def draw(self, surface):
        # shaft with two circles at each end (classic bone shape)
        ...