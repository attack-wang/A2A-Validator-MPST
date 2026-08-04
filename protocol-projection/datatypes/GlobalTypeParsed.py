from enum import Enum

from datatypes.MessageSndRcv import MessageSndRcv, MessageSndRcvKinds
from datatypes.classical_projection.AvailabilitySet import AvailabilitySet
from datatypes.classical_projection.LocalType import LocalType, LocalTypeKinds
from datatypes.classical_projection.UnionAvailabilitySet import UnionAvailabilitySet


# a class for global types as parsed from files or input (no additional information yet)
class GlobalTypeParsed:

    def __init__(self, kind, data):
        # depending on the kind, data is different
        # we assume consistency of provided data
        self.kind = kind
        if kind == GlobalTypeKinds.NULLTYPE:
            pass
        elif kind == GlobalTypeKinds.CHOICE:
            assert len(data) > 0
            # we assume that sender is the same across all
            self.options = data             # list of pairs with msg_exchange and continuation
        elif kind == GlobalTypeKinds.RECURSION:
            self.bound_variable = data[0]      # bound variable in string representation
            self.continuation = data[1]
            # we check that no recursion variable is bound in the same scope twice
            if self.bound_variable in self.continuation.get_all_binders():
                raise Exception('Variable bound twice in the same scope.')
            # we assume that each variable use is bound
        elif kind == GlobalTypeKinds.REC_VAR:
            self.ref_variable = data        # referred variable in string representation
        else:
            raise Exception('Global type has no kind.')

    def __str__(self):
        return self.str_helper(0)

    # helper function to produce string representation
    def str_helper(self, num_tabs):
        if self.kind == GlobalTypeKinds.NULLTYPE:
            return '0'
        elif self.kind == GlobalTypeKinds.CHOICE:
            if len(self.options) == 1:
                return str(self.options[0][0]) + '. ' + self.options[0][1].str_helper(num_tabs)
            else:
                num_tabs += 1
                prefix = ''.join(['\t'] * num_tabs)
                result = '( \n' + prefix
                result += (' \n ' + prefix + '+ \n' + prefix).join((str(x[0]) + '. ' + x[1].str_helper(num_tabs)) for x in self.options)
                result += '\n' + prefix + ')'
                return result
        elif self.kind == GlobalTypeKinds.RECURSION:
            return 'μ ' + self.bound_variable + '. ' + self.continuation.str_helper(num_tabs)
        elif self.kind == GlobalTypeKinds.REC_VAR:
            return self.ref_variable

    # returns all processes in a protocol
    def get_procs(self):
        result = self.get_procs_helper()
        return sorted(result)

    # is an internal helper function to obtain all processes
    def get_procs_helper(self):
        if self.kind == GlobalTypeKinds.CHOICE:
            result = set()
            for o in self.options:
                result.update(o[0].get_procs())
                result.update(o[1].get_procs_helper())
            return result
        elif self.kind == GlobalTypeKinds.RECURSION:
            return self.continuation.get_procs_helper()
        else:
            return set()

    # returns all binders
    def get_all_binders(self):
        if self.kind == GlobalTypeKinds.CHOICE:
            result = set()
            for o in self.options:
                comp_result = o[1].get_all_binders()
                result.update(comp_result)
            return result
        elif self.kind == GlobalTypeKinds.RECURSION:
            result = self.continuation.get_all_binders()
            result.update([self.bound_variable])
            return result
        else:
            return set()

    # returns all unique binders
    def set_of_unique_binders(self):
        if self.kind == GlobalTypeKinds.CHOICE:
            result = set()
            for o in self.options:
                comp_result = o[1].set_of_unique_binders()
                if comp_result is None:
                    return None
                both_num = len(result) + len(comp_result)
                result.update(comp_result)
                if not both_num == len(result):
                    return None
            return result
        elif self.kind == GlobalTypeKinds.RECURSION:
            result = self.continuation.set_of_unique_binders()
            result.update([self.bound_variable])
            return result
        else:
            return set()

    # computes the size of a global type as is standard
    def get_size(self):
        if self.kind == GlobalTypeKinds.NULLTYPE:
            return 1
        elif self.kind == GlobalTypeKinds.CHOICE:
            res = len(self.options)
            for option in self.options:
                res += option[1].get_size()
            return res
        elif self.kind == GlobalTypeKinds.RECURSION:
            return 1 + self.continuation.get_size()
        elif self.kind == GlobalTypeKinds.REC_VAR:
            return 1

    # computes the set of (directed) channels that are used
    def get_used_channels(self):
        if self.kind == GlobalTypeKinds.NULLTYPE:
            return set()
        elif self.kind == GlobalTypeKinds.CHOICE:
            channels = set()
            for option in self.options:
                channels.add((option[0].sender, option[0].receiver))
                channels.update(option[1].get_used_channels())
            return channels
        elif self.kind == GlobalTypeKinds.RECURSION:
            return self.continuation.get_used_channels()
        elif self.kind == GlobalTypeKinds.REC_VAR:
            return set()

    # computes a map from recursion variables to the subterm they were bound at
    def compute_rec_var_map(self):
        # we assume uniqueness of all bound variables across branches in calling context
        if self.kind == GlobalTypeKinds.CHOICE:
            result = list()
            for o in self.options:
                result.extend(o[1].compute_rec_var_map())
            return result
        elif self.kind == GlobalTypeKinds.RECURSION:
            result = self.continuation.compute_rec_var_map()
            result.append((self.bound_variable, self.continuation))
            return result
        else:
            return list()

    # applies classical projection for a process
    def project_onto(self, process, vars_empty, rec_var_map):
        if self.kind == GlobalTypeKinds.NULLTYPE:
            return LocalType(LocalTypeKinds.NULLTYPE, None, # set(),
                             AvailabilitySet(self, process, set(), set(), rec_var_map, vars_empty))
        elif self.kind == GlobalTypeKinds.CHOICE:
            # 1) Process is sender
            if self.options[0][0].sender == process:
                list_conts = []
                for option in self.options:
                    proj_msg_exc = option[0].project_onto(process)
                    proj_cont = option[1].project_onto(process, set(), rec_var_map)
                    list_conts.append((proj_msg_exc, proj_cont))
                return LocalType(LocalTypeKinds.INTCHOICE,
                                 list_conts,
                                 AvailabilitySet(self, process, set(), set(), rec_var_map, vars_empty)
                                 )
            # 2) now, process can either not be part of exchange or the receiver
            else:
                list_to_merge = []
                # sort continuations where process is part of msg exchange (as receiver) or not
                list_part_of_msg_exc = list(filter(lambda o: o[0].receiver == process, self.options))
                if len(list_part_of_msg_exc) > 0:
                    options_part_of_msg_exc = []
                    for option in list_part_of_msg_exc:
                        options_part_of_msg_exc.append((option[0].project_onto(process),
                                                        option[1].project_onto(process, set(), rec_var_map)))
                    # COMPUTE AVAIL
                    lazy_avail_sets = []
                    for option in list_part_of_msg_exc:
                        lazy_avail_sets.append(AvailabilitySet(option, process, set(), set(), rec_var_map, vars_empty))
                    list_to_merge.append(LocalType(LocalTypeKinds.EXTCHOICE, options_part_of_msg_exc,
                                                   UnionAvailabilitySet(lazy_avail_sets)
                                                   ))
                list_not_part_of_msg_exc = list(filter(lambda o: o[0].receiver != process, self.options))
                for option in list_not_part_of_msg_exc:
                    # not part of msg_exc so we omit to project to an empty one here
                    proj_cont = option[1].project_onto(process, vars_empty, rec_var_map)
                    # check whether the continuation is
                    is_rec_for_one = False
                    for rec_var in vars_empty:
                        if proj_cont.kind == LocalTypeKinds.REC_VAR and proj_cont.ref_variable == rec_var:
                            is_rec_for_one = True
                            break
                    if not is_rec_for_one:
                        list_to_merge.append(proj_cont)
                return LocalType.merge(list_to_merge, process)
        elif self.kind == GlobalTypeKinds.RECURSION:
            proj_cont = self.continuation.project_onto(process, {self.bound_variable}.union(vars_empty), rec_var_map)
            is_bound_variable_itself = proj_cont.kind == LocalTypeKinds.REC_VAR and \
                                       proj_cont.ref_variable == self.bound_variable
            bound_variable_occurs = proj_cont.rec_var_occurs(self.bound_variable)
            # ignore if loop to be ignored
            if proj_cont.kind == LocalTypeKinds.IGNORE:
                return LocalType(LocalTypeKinds.NULLTYPE, None, # set(),
                                 AvailabilitySet(self, process, set(), set(), rec_var_map, vars_empty)
                                 )
            if not is_bound_variable_itself and bound_variable_occurs:
                return LocalType(LocalTypeKinds.RECURSION, (self.bound_variable, proj_cont),
                                 AvailabilitySet(self, process, set(), set(), rec_var_map, vars_empty)
                                 )
            elif not bound_variable_occurs:
                # avail_msgs = self.continuation.avail_msgs(process, {process}, {self.bound_variable}, rec_var_map)
                # proj_cont.lazy_avail = AvailabilitySet(self.continuation, process, {process}, {self.bound_variable}, rec_var_map, vars_empty)
                return proj_cont
            else:
                return LocalType(LocalTypeKinds.NULLTYPE, None, # set(),
                                 AvailabilitySet(self, process, set(), set(), rec_var_map, vars_empty)
                                 )
        elif self.kind == GlobalTypeKinds.REC_VAR:
            res = LocalType(LocalTypeKinds.REC_VAR, self.ref_variable,
                            AvailabilitySet(self, process, set(), set(), rec_var_map, vars_empty)
                            )
            return res
        else:
            raise Exception('how did we get here?')

    # computes the set of available messages syntactically on the global type (used for classical projection)
    # In contrast to the general definition, we filter all the irrelevant, i.e. message events by other processes, before returning
    def avail_msgs(self, process, blocked_procs, handled_vars, rec_var_map):
        if self.kind == GlobalTypeKinds.NULLTYPE:
            return set()
        elif self.kind == GlobalTypeKinds.CHOICE:
            # recall that sender is the same across all branches
            if self.options[0][0].sender in blocked_procs:
                avail_msgs = set()
                for option in self.options:
                    next_blocked_procs = {option[0].receiver}.union(blocked_procs)
                    cont_avail_msgs = option[1].avail_msgs(process, next_blocked_procs, handled_vars, rec_var_map)
                    avail_msgs.update(cont_avail_msgs)
                # return the set sorted for process
                return MessageSndRcv.set_project_onto(process, avail_msgs)
            else:
                msgs_cont = set()
                for option in self.options:
                    msgs_cont_single = option[1].avail_msgs(process, blocked_procs, handled_vars, rec_var_map)
                # only keep FIFO-ordered messages
                    msgs_possible = list(filter(lambda mex: not mex.sender == option[0].sender or not mex.receiver == option[0].receiver,
                                            msgs_cont_single))
                    msgs_cont.update(msgs_possible)
                # add the ones from the option
                for option in self.options:
                    msgs_cont.add(MessageSndRcv(MessageSndRcvKinds.RCV, option[0].sender, option[0].receiver, option[0].message))
                # return the set sorted for process
                return MessageSndRcv.set_project_onto(process, msgs_cont)
        elif self.kind == GlobalTypeKinds.RECURSION:
            next_handled_vars = {self.bound_variable}.union(handled_vars)
            return self.continuation.avail_msgs(process, blocked_procs, next_handled_vars, rec_var_map)
        elif self.kind == GlobalTypeKinds.REC_VAR:
            if self.ref_variable in handled_vars:
                return set()
            else:
                next_handled_vars = {self.ref_variable}.union(handled_vars)
                where_to_cont = rec_var_map[self.ref_variable]
                avail_msgs_there = where_to_cont.avail_msgs(process, blocked_procs, next_handled_vars, rec_var_map)
                return avail_msgs_there


    @staticmethod
    # compares if two global types are structurally the same
    # Since we do not swap branches, this overapproximates optimal solution but is fine
    def compare_global_types(globaltype1, globaltype2):
        worklist = [(globaltype1, globaltype2)]
        bound_variables = dict()
        while len(worklist) > 0:
            current1, current2 = worklist.pop()
            if current1.kind == GlobalTypeKinds.NULLTYPE and current2.kind == GlobalTypeKinds.NULLTYPE:
                pass
            elif current1.kind == GlobalTypeKinds.CHOICE and current2.kind == GlobalTypeKinds.CHOICE:
                if len(current1.options) != len(current2.options):
                    return False
                for i in range(0, len(current1.options)):
                    if current1.options[i][0] != current2.options[i][0]:
                        return False
                    worklist.append((current1.options[i][1], current2.options[i][1]))
            elif current1.kind == GlobalTypeKinds.RECURSION and current2.kind == GlobalTypeKinds.RECURSION:
                bound_variables[current1.bound_variable] = current2.bound_variable
                worklist.append((current1.continuation, current2.continuation))
            elif current1.kind == GlobalTypeKinds.REC_VAR and current2.kind == GlobalTypeKinds.REC_VAR:
                if current1.ref_variable == current2.ref_variable:
                    pass
                else:
                    bound_before = bound_variables.get(current1.ref_variable)
                    if bound_before is None or bound_before != current2.ref_variable:
                        return False
            else:
                return False
        return True


# defines the different kinds for global types
class GlobalTypeKinds(Enum):
    NULLTYPE = 'n'
    CHOICE = 'c'
    RECURSION = 'r'
    REC_VAR = 'v'
