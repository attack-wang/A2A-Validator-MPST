class MysteryBag(GameObject):
    NAME = "mystery bag"
    VALUE = 0  # determined when grabbed
    WEIGHT = 1.2
    RADIUS = 18
    POSSIBLE_VALUES = [50, 100, 250, 500, 750]
    def reveal(self):
        self.value = random.choice(self.POSSIBLE_VALUES)
        return self.value