from __future__ import annotations

from datatypes.MessageSndRcv import MessageSndRcv
from datatypes.subset_projection.SuperState import SuperState


# a class to store finite state machines for a process
class LocalFSM:

    def __init__(self,
                 initial_superstate : SuperState,
                 map_superstate_trans_superstate : dict[SuperState, list[tuple[MessageSndRcv, SuperState]]]):
        self.initial_superstate : SuperState = initial_superstate
        self.map_superstate_trans_superstate : dict[SuperState, list[tuple[MessageSndRcv, SuperState]]] = map_superstate_trans_superstate

    def __str__(self) -> str:
        result = ""
        result += "Initial State: " + str(self.initial_superstate) + "\n"
        result += "Transitions: \n"
        for key, value in reversed(self.map_superstate_trans_superstate.items()):
            result += str(key) + ": "
            for msg, state in value:
                result += "\n\t(" + str(msg) + ", " + str(state) + ")"
            result += "\n"
        return result

    def get_size(self):
        size = 0
        visited = set()
        worklist = [self.initial_superstate]
        while len(worklist) > 0:
            to_expand = worklist.pop(0)
            size += 1
            visited.add(to_expand)
            list_of_transitions = self.map_superstate_trans_superstate.get(to_expand, [])
            size += len(list_of_transitions)
            for _, next_superstate in list_of_transitions:
                if next_superstate not in visited:
                    worklist.append(next_superstate)
        return size