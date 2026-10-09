from __future__ import annotations
from datatypes.MessageSndRcv import MessageSndRcv, MessageSndRcvEmpty
from datatypes.subset_projection.State import State

from typing import Union

from datatypes.subset_projection.SuperState import SuperState

# a class that projects each transition label of a globaltype_fsm onto a process
class ProjectionByErasure:

    def __init__(self, globaltype_fsm, process: str):
        # we basically do a breadth-first search through the globaltype fsm
        self.map_state_trans_state : dict[State, list[tuple[Union[MessageSndRcv, MessageSndRcvEmpty], State]]] = dict()
        worklist = [globaltype_fsm.initial_state]
        visited = set()
        while len(worklist) != 0:
            current_state = worklist.pop(0)
            trans_targets = globaltype_fsm.map_state_to_list_trans_state.get(current_state)
            list_trans_targets : list[tuple[Union[MessageSndRcv, MessageSndRcvEmpty], State]] = []
            for transition, target in trans_targets:
                new_transition = transition.project_onto(process)
                list_trans_targets.append((new_transition, target))
                if target not in visited:
                    worklist.append(target)
                    visited.add(target)
            self.map_state_trans_state[current_state] = list_trans_targets
        # empty initialization of cache
        self.memo_transitions_from_to : dict[State, list[tuple[MessageSndRcv, State]]] = dict()
        self.cache_epsilon_hull : dict[State, list[State]] = dict()

    # given a state, we compute the non-epsilon transitions and target states
    # we compute (non-epsilon, epsilon^*)-transitions
    # (as we know that we always do this and keep all states in a superstate)
    def transitions_from_to(self, state) -> list[tuple[MessageSndRcv, State]]:
        intermediate_result : set[tuple[MessageSndRcv, State]] = set()
        # first, get all next states with immediate transition
        for transition, target in self.map_state_trans_state[state]:
            if type(transition) is MessageSndRcv:
                intermediate_result.add((transition, target))
        # second, build the epsilon-hull for these
        result = set()
        for non_empty_transition, next_state in intermediate_result:
            result.add((non_empty_transition, next_state))
            list_epsilon_successors = self.epsilon_hull(next_state)
            for epsilon_successor in list_epsilon_successors:
                result.add((non_empty_transition, epsilon_successor))
        return list(result)

    # computes a superstate consisting of all states reachable with epsilon-transitions
    def superstate_of_epsilon_hull(self, state) -> SuperState:
        return SuperState(self.epsilon_hull(state))

    # computes the epsilon-hull of a state
    def epsilon_hull(self, state) -> list[State]:
        cached_result = self.cache_epsilon_hull.get(state)
        if cached_result is not None:
            return cached_result
        worklist = [state]
        result = {state}
        while len(worklist) != 0:
            current_state = worklist.pop(0)
            list_trans_target = self.map_state_trans_state[current_state]
            for trans, target in list_trans_target:
                if type(trans) == MessageSndRcvEmpty and target not in result:
                    result.add(target)
                    worklist.append(target)
        list_result = list(result)
        self.cache_epsilon_hull[state] = list_result
        return list_result


    def __str__(self) -> str:
        result = ""
        result += "Transitions: \n"
        for key, value in self.map_state_trans_state.items():
            result += str(key) + ": "
            for msg, state in value:
                result += "\n\t(" + str(msg) + ", " + str(state) + ")"
            result += "\n"
        result += "\n"
        return result
