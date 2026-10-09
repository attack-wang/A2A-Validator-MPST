from __future__ import annotations

import itertools
import os
from enum import Enum

from datatypes.GlobalTypeParsed import GlobalTypeParsed, GlobalTypeKinds
from datatypes.subset_projection.LocalFSM import LocalFSM
from datatypes.MessageExchange import MessageExchange, MessageExchangeEmpty
from datatypes.MessageSndRcv import MessageSndRcv, MessageSndRcvKinds
from datatypes.subset_projection.ProjectionByErasure import ProjectionByErasure
from datatypes.subset_projection.State import State
from collections import defaultdict

from typing import Union, Optional

from datatypes.subset_projection.SuperState import SuperState

# a class to store a global type as a finite state machine
class GlobalTypeFSM:

    def __init__(self, globaltype: GlobalTypeParsed):
        # store the subterm for each state
        self.map_state_to_subterm : dict[State, GlobalTypeParsed] = dict()
        # store a list of transitions and target states for each state
        self.map_state_to_list_trans_state : dict[State, list[tuple[Union[MessageExchange, MessageExchangeEmpty], State]]] = dict()
        # for each recursion variable, store the state where it is bound
        self.map_rec_var_to_state : dict[str, State] = dict() # maps recursion variable as string to respective State
        # store which the next state id is available (ids are used to quickly distinguish states)
        self.next_state_id = 0
        # generate a cache of subterms to states
        self.cache_subterm_state_list : list[(GlobalTypeParsed, State)] = []
        # compute size on the fly
        self.size = 0
        # generate the finite state machine and store the initial state
        self.initial_state = self.generate_FSM(globaltype)

    # used in __init__
    def generate_FSM(self, subterm) -> State:
        # get a state for the current subterm and recursively compute the transitions
        state_for_subterm : State = self.get_next_state(subterm)
        self.map_state_to_subterm[state_for_subterm] = subterm
        if subterm.kind == GlobalTypeKinds.NULLTYPE:
            state_for_subterm.is_final = True
            self.map_state_to_list_trans_state[state_for_subterm] = []
        elif subterm.kind == GlobalTypeKinds.CHOICE:
            trans_state_list : list[tuple[Union[MessageExchange, MessageExchangeEmpty], State]] = []
            for msg_exchange, continuation in subterm.options: # list of pairs with msg_exchange and continuation
                state_for_continuation = self.generate_FSM(continuation)
                trans_state_list.append((msg_exchange, state_for_continuation))
            self.map_state_to_list_trans_state[state_for_subterm] = trans_state_list
            self.size += len(trans_state_list)
        elif subterm.kind == GlobalTypeKinds.RECURSION:
            self.map_rec_var_to_state[subterm.bound_variable] = state_for_subterm
            state_for_continuation = self.generate_FSM(subterm.continuation)
            self.map_state_to_list_trans_state[state_for_subterm] = [(MessageExchangeEmpty(), state_for_continuation)]
            self.size += 1
        elif subterm.kind == GlobalTypeKinds.REC_VAR:
            binder_state = self.map_rec_var_to_state.get(subterm.ref_variable)
            assert binder_state is not None
            self.map_state_to_list_trans_state[state_for_subterm] = [(MessageExchangeEmpty(), binder_state)]
        else:
            raise Exception('Global type has no valid kind.')
        return state_for_subterm

    def get_next_state(self, subterm) -> State:
        # check against previously seen subterms
        for cached_subterm, cached_state in self.cache_subterm_state_list:
            if GlobalTypeParsed.compare_global_types(cached_subterm, subterm):
                return cached_state
        # if not found, generate it
        state_for_subterm = State(self.next_state_id)
        self.cache_subterm_state_list.append((subterm, state_for_subterm))
        self.next_state_id += 1
        self.size += 1
        return state_for_subterm

    def get_size(self):
        return self.size

    def project_onto(self, proc) -> Optional[LocalFSM]:
        # 1) compute a projection by erasure onto the process so that the checks are faster later (not determinising)
        projection_by_erasure = ProjectionByErasure(self, proc)
        # 2) generate the subset projection
        map_superstate_trans_superstate : dict[SuperState, list[tuple[MessageSndRcv, SuperState]]] = dict()
        # we compute the initial super state using an epsilon-hull
        initial_superstate : SuperState = projection_by_erasure.superstate_of_epsilon_hull(self.initial_state)
        # we basically do a breadth-first search, starting from the initial super state
        worklist = [initial_superstate]
        while len(worklist) != 0:
            current_superstate = worklist.pop(0)
            # we first compute the all possible transitions from each state in the super state
            # (only first non-epsilon, then epsilon)
            map_state_transitions_targets : dict[State, list[tuple[MessageSndRcv, State]]] = dict()
            for state in current_superstate.states:
                map_state_transitions_targets[state] = projection_by_erasure.transitions_from_to(state)
            # given this list for each state, we check our validity conditions
            # and, if satifsied, we generate the transitions if
            list_transitions : Optional[list[tuple[MessageSndRcv, SuperState]]] = \
                self.check_validity_conditions_and_generate_transitions(proc, current_superstate, projection_by_erasure, map_state_transitions_targets)
            # if the validity conditions are satisfied,
            # we add the transitions to the local FSM and the target states to the worklist
            if list_transitions is not None:
                map_superstate_trans_superstate[current_superstate] = list_transitions
                for _, next_superstate in list_transitions:
                    if next_superstate not in map_superstate_trans_superstate.keys():
                        worklist.append(next_superstate)
            else:
                return None
        return LocalFSM(initial_superstate, map_superstate_trans_superstate)

    def check_validity_conditions_and_generate_transitions(self, proc, super_state, projection_by_erasure, map_state_transitions_targets) \
            -> Optional[list[tuple[MessageSndRcv, SuperState]]]:
        type_choice: LocalChoiceType = GlobalTypeFSM.which_type_of_local_choice(map_state_transitions_targets)
        if type_choice == LocalChoiceType.MIXEDCHOICE:
            return None
        elif type_choice == LocalChoiceType.NO_TRANSITIONS:
            # the super_state is either final as it contains 0 OR
            # there is no 0 reachable from here and thus only infinite executions and it is fine to have a non-final sink state
            return []
        try:
            if type_choice == LocalChoiceType.SEND:
                return GlobalTypeFSM.check_send_conditions_and_generate_transitions(super_state, projection_by_erasure, map_state_transitions_targets)
            elif type_choice == LocalChoiceType.RECEIVE:
                return self.check_receive_conditions_and_generate_transitions(proc, map_state_transitions_targets)
        except: # previous raise Exception if validity is violated, so we return None
            return None
        raise Exception("Local choice type was neither mixed, internal nor external. This should not be possible!")

    @staticmethod
    def which_type_of_local_choice(map_state_transitions_targets : dict[State, list[tuple[MessageSndRcv, State]]]) -> LocalChoiceType:
        # compute a list of all transitions and targets
        list_all_transitions_and_targets = []
        for list_transitions_targets in map_state_transitions_targets.values():
            list_all_transitions_and_targets.extend(list_transitions_targets)
        # check if there are any transitions
        if len(list_all_transitions_and_targets) == 0:
            return LocalChoiceType.NO_TRANSITIONS
        # filter the ones where the transition is a send
        list_all_transitions_SND = [transition.kind == MessageSndRcvKinds.SND for transition, _ in list_all_transitions_and_targets]
        # if all transitions are sends, the local choice type is internal
        if all(list_all_transitions_SND):
            return LocalChoiceType.SEND
        # if only some transitions are sends, the local choice type is mixed
        if any(list_all_transitions_SND):
            return LocalChoiceType.MIXEDCHOICE
        # otherwise, they are all receives and, thus, the local choice type is external
        return LocalChoiceType.RECEIVE

    @staticmethod
    def check_send_conditions_and_generate_transitions(super_state, projection_by_erasure, map_state_to_transitions_and_targets) -> Optional[list[tuple[MessageSndRcv, SuperState]]]:
        validity_checks = os.getenv('VALIDITY_CHECK')
        if validity_checks != "FALSE":
            # we first compute all state origins with an immediate non-epsilon transition
            all_origins_with_immediate_transitions = [origin for origin in map_state_to_transitions_and_targets.keys() if len(map_state_to_transitions_and_targets[origin]) != 0]
            all_origins_without_transitions = [origin for origin in map_state_to_transitions_and_targets.keys() if len(map_state_to_transitions_and_targets[origin]) == 0]
            # first check that every origin without transition is connected to some with
            for origin_without in all_origins_without_transitions:
                if all([origin_with not in projection_by_erasure.epsilon_hull(origin_without) for origin_with in all_origins_with_immediate_transitions]):
                    raise Exception("Send State Val not satisfied")
            # second check that the ones with transition agree
            default_transitions = [transition for transition, _ in map_state_to_transitions_and_targets[all_origins_with_immediate_transitions[0]]]
            # first check that all transitions originate in all the possible states
            # we actually take a non-epsilon, epsilon-hull - approach so a transition might not origin in a state
            # but in one that is connected via epsilon-transitions
            for other_origin in all_origins_with_immediate_transitions[1:]:
                other_transitions = [transition for transition, _ in map_state_to_transitions_and_targets[other_origin]]
                if set(default_transitions) != set(other_transitions):
                    # Send State Validity not given
                    raise Exception("Send State Val not satisfied")
                    # return None
        # second actually generate the transitions
        list_transitions = GlobalTypeFSM.generate_transitions_after_condition_check(map_state_to_transitions_and_targets)
        return list_transitions

    def check_receive_conditions_and_generate_transitions(self, proc, map_state_transitions_targets) -> Optional[list[tuple[MessageSndRcv, SuperState]]]:
        validity_checks = os.getenv('VALIDITY_CHECK')
        if validity_checks != "FALSE":
            # we compute a map from transitions to where they origin
            map_transition_to_origins : dict[MessageSndRcv, set[State]] = defaultdict(lambda : set())
            for originates, transitiontargetlist in map_state_transitions_targets.items():
                for transitiontarget in transitiontargetlist:
                    map_transition_to_origins[transitiontarget[0]].add(originates)
            all_transitions = list(map_transition_to_origins.keys())
            # we check if all the same sender, then we do not need to generate all pairs of transitions
            first_transition = list(all_transitions)[0]
            all_same_sender = all(first_transition.sender == other_transition.sender for other_transition in all_transitions)
            # if there are different senders, ...
            if not all_same_sender:
                # we consider all pairs
                for trans1, trans2 in itertools.combinations(all_transitions, 2):
                    # again, if the senders are different for this pair,
                    # we compute the available messages for both and check absense
                    # (for the continuations of the respective transition respectively)
                    if trans1.sender != trans2.sender:
                        for state in map_transition_to_origins[trans1]:
                            avail_msgs1 = self.avail_msgs(proc, state, trans1)
                            if trans2 in avail_msgs1:
                                raise Exception("RCV State Val not satisfied")
                        for state in map_transition_to_origins[trans2]:
                            avail_msgs2 = self.avail_msgs(proc, state, trans2)
                            if trans1 in avail_msgs2:
                                raise Exception("RCV State Val not satisfied")
        # we reach this if all validity checks were successful, so we generate the transitions
        list_transitions = GlobalTypeFSM.generate_transitions_after_condition_check(map_state_transitions_targets)
        return list_transitions

    # computes the available messages for a state and a transition under consideration
    def avail_msgs(self, proc, state, taken_trans) -> set[MessageSndRcv]:
        # we need to consider the available messages of the continuation,
        # ow., we easily prohibit transitions that are possible from the same state
        # we first search for the next state
        next_state = None
        for poss_trans, poss_next_state in self.map_state_to_list_trans_state[state]:
            if poss_trans.project_onto(proc) == taken_trans:
                next_state = poss_next_state
                break
        # assert that the next state for the given transition was found
        assert next_state is not None
        # actually compute the available messages from this next state
        return self.compute_avail_msgs(proc, next_state, {proc}, set(), set(), True)

    def compute_avail_msgs(self, proc, state, blocked_procs, visited, ignore_from, is_first_state) \
            -> set[MessageSndRcv]:
        # ignore_from contains all the senders from which messages can be ignored in this path
        # because there is an earlier one already
        avail_msgs = set()
        # we basically do a breadth-first search
        # we ensure that we check long enough by not adding the first state we consider when visiting it the first time
        if is_first_state:
            is_first_state = False
        else:
            visited.add(state)
        for trans, next_state in self.map_state_to_list_trans_state[state]:
            # a) compute the message which comes from this transition and update ignore_from if necessary
            projected_trans = trans.project_onto(proc)
            if type(projected_trans) is MessageSndRcv:
                if projected_trans.kind == MessageSndRcvKinds.RCV:
                    if projected_trans.sender not in ignore_from and projected_trans.sender not in blocked_procs:
                        avail_msgs.add(projected_trans)
                        ignore_from.add(projected_trans.sender)
            if next_state not in visited:
                # b) compute the new set of blocked procs
                if type(trans) is MessageExchange and trans.sender in blocked_procs:
                    blocked_procs.add(trans.receiver)
                # c) compute the subsequent messages and join them
                subsequent_messages = self.compute_avail_msgs(proc, next_state, blocked_procs.copy(), visited.copy(), ignore_from.copy(), is_first_state)
                avail_msgs = avail_msgs.union(subsequent_messages)
        return avail_msgs

    @staticmethod
    def generate_transitions_after_condition_check(map_state_transitions_targets) -> list[tuple[MessageSndRcv, SuperState]]:
        all_origins = map_state_transitions_targets.keys()
        map_transitions_to_next_states : defaultdict[MessageSndRcv, set[State]] = defaultdict(lambda: set())
        for origin in all_origins:
            for transition, next_state in map_state_transitions_targets[origin]:
                map_transitions_to_next_states[transition].add(next_state)
        return [(transition, SuperState(list(setstates))) for transition, setstates in
                list(map_transitions_to_next_states.items())]

    def __str__(self) -> str:
        result = ""
        result += "Initial State: " + str(self.initial_state) + "\n"
        result += "Transitions: \n"
        for key, value in reversed(self.map_state_to_list_trans_state.items()):
            result += str(key) + ": "
            for msg, state in value:
                result += "\n\t(" + str(msg) + ", " + str(state) + ")"
            result += "\n"
        result += "\n"
        result += "Subterm Map: \n"
        for key, value in self.map_state_to_subterm.items():
            result += str(key) + ": \n\t" + str(value)
            result += "\n"
        return result


# defines the different kinds choice of local states
class LocalChoiceType(Enum):
    NO_TRANSITIONS = 'n'
    MIXEDCHOICE = 'm'
    SEND = 'i'
    RECEIVE = 'e'
