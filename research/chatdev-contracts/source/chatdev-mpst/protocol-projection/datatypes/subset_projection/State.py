# a class for a state, which can be final or not
class State:

    def __init__(self, id : int, is_final : bool = False):
        self.id : int = id
        self.is_final : bool = is_final

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return str(self.id)

    def __eq__(self, obj):
        return self.id == obj.id