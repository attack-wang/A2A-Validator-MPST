from datatypes.subset_projection.State import State

# a class that stores a list of states
class SuperState:

    def __init__(self, states : list[State]):
        self.states : list[State] = states

    def is_final(self):
        return any(state.is_final for state in self.states)

    def __hash__(self):
        return hash(tuple(self.states))

    def __str__(self):
        is_final = any(state.is_final for state in self.states)
        final_suffix = "f" if is_final else "n"
        return "{ " + ", ".join([str(state) for state in self.states]) + " }_" + final_suffix

    def __eq__(self, obj):
        return set(self.states) == set(obj.states)