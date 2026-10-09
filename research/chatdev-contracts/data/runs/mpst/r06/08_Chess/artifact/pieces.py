    def copy(self):
        cls = type(self)
        dup = cls(self.color)
        dup.has_moved = self.has_moved
        return dup