from datatypes.MessageSndRcv import *
from datatypes.classical_projection.ProjectionUndefined import *
# from datatypes.GlobalType import GlobTypeKinds
from datatypes.classical_projection.UnionAvailabilitySet import *


class LocalType:
    def __init__(self, kind, data, lazy_avail):
        self.kind = kind
        self.lazy_avail = lazy_avail
        if type(lazy_avail) is set:
            pass
        if lazy_avail is None and kind is not LocalTypeKinds.IGNORE:
            print('why is avail empty?')
        if kind == LocalTypeKinds.NULLTYPE:
            pass
        elif kind == LocalTypeKinds.INTCHOICE:
            # for multiple choices, we convert to a dict for comparison (only for local types needed for now)
            self.options = dict(data)  # dict of pairs with msg_send or msg_rcv and continuation
        elif kind == LocalTypeKinds.EXTCHOICE:
            # for multiple choices, we convert to a dict for comparison (only for local types needed for now)
            self.options = dict(data)  # list of pairs with msg_send or msg_rcv and continuation
        elif kind == LocalTypeKinds.RECURSION:
            self.bound_variable = data[0]  # bound variable in string representation
            self.continuation = data[1]
        elif kind == LocalTypeKinds.REC_VAR:
            self.ref_variable = data  # referred variable in string representation

    def __str__(self):
        return self.str_helper(0)

    def __hash__(self):
        return hash(str(self))

    def str_helper(self, num_tabs):
        if self.kind == LocalTypeKinds.NULLTYPE:
            return '0'
        elif self.kind == LocalTypeKinds.INTCHOICE:
            if len(self.options) == 1:
                for item in self.options.items():
                    return str(item[0]) + '. ' + item[1].str_helper(num_tabs)
            else:
                num_tabs += 1
                prefix = ''.join(['\t'] * num_tabs)
                result = '( \n' + prefix
                result += (' \n ' + prefix + '+ \n' + prefix).join(
                    (str(x[0]) + '. ' + x[1].str_helper(num_tabs)) for x in self.options.items())
                result += '\n' + prefix + ')'
                return result
        elif self.kind == LocalTypeKinds.EXTCHOICE:
            if len(self.options) == 1:
                for item in self.options.items():
                    return str(item[0]) + '. ' + item[1].str_helper(num_tabs)
            else:
                num_tabs += 1
                prefix = ''.join(['\t'] * num_tabs)
                result = '( \n' + prefix
                result += (' \n ' + prefix + '& \n' + prefix).join(
                    (str(x[0]) + '. ' + x[1].str_helper(num_tabs)) for x in self.options.items())
                result += '\n' + prefix + ')'
                return result
        elif self.kind == LocalTypeKinds.RECURSION:
            return 'μ ' + self.bound_variable + '. ' + self.continuation.str_helper(num_tabs)
        elif self.kind == LocalTypeKinds.REC_VAR:
            return self.ref_variable

    def __eq__(self, other):
        return vars(self) == vars(other)

    # subst_var changes the local type and does not return a new one
    def subst_var(self, to_subst, subst_by):
        if self.kind == LocalTypeKinds.NULLTYPE:
            pass
        elif self.kind == LocalTypeKinds.INTCHOICE or self.kind == LocalTypeKinds.EXTCHOICE:
            for cont in self.options.values():
                cont.subst_var(to_subst, subst_by)
        elif self.kind == LocalTypeKinds.RECURSION:
            if self.bound_variable == to_subst:
                self.bound_variable = subst_by
            self.continuation.subst_var(to_subst, subst_by)
        elif self.kind == LocalTypeKinds.REC_VAR:
            if self.ref_variable == to_subst:
                self.ref_variable = subst_by

    def rec_var_occurs(self, rec_var):
        if self.kind == LocalTypeKinds.NULLTYPE:
            return False
        elif self.kind == LocalTypeKinds.INTCHOICE or self.kind == LocalTypeKinds.EXTCHOICE:
            for cont in self.options.values():
                if cont.rec_var_occurs(rec_var):
                    return True
            return False
        elif self.kind == LocalTypeKinds.RECURSION:
            return self.continuation.rec_var_occurs(rec_var)
        elif self.kind == LocalTypeKinds.REC_VAR:
            if self.ref_variable == rec_var:
                return True
            else:
                return False

    def set_of_unique_binders(self):
        if self.kind == LocalTypeKinds.INTCHOICE or self.kind == LocalTypeKinds.EXTCHOICE:
            result = set()
            for o in self.options.items():
                comp_result = o[1].set_of_unique_binders()
                if comp_result is None:
                    return None
                both_num = len(result) + len(comp_result)
                result.update(comp_result)
                if not both_num == len(result):
                    return None
            return result
        elif self.kind == LocalTypeKinds.RECURSION:
            result = self.continuation.set_of_unique_binders()
            result.update([self.bound_variable])
            return result
        else:
            return set()

    def compute_rec_var_map(self):
        # we assert uniqueness of all bound variables across branches in calling context
        if self.kind == LocalTypeKinds.INTCHOICE or self.kind == LocalTypeKinds.EXTCHOICE:
            result = list()
            for o in self.options.items():
                result.extend(o[1].compute_rec_var_map())
            return result
        elif self.kind == LocalTypeKinds.RECURSION:
            result = self.continuation.compute_rec_var_map()
            result.append((self.bound_variable, self.continuation))
            return result
        else:
            return list()

    def is_defined(self):
        return self.no_ignore()

    def no_ignore(self):
        if self.kind == LocalTypeKinds.NULLTYPE:
            return True
        elif self.kind == LocalTypeKinds.INTCHOICE or self.kind == LocalTypeKinds.EXTCHOICE:
            for cont in self.options.values():
                if not cont.no_ignore():
                    return False
            return True
        elif self.kind == LocalTypeKinds.RECURSION:
            return self.continuation.no_ignore()
        elif self.kind == LocalTypeKinds.REC_VAR:
            return True
        elif self.kind == LocalTypeKinds.IGNORE:
            return False

    def congruent_wo_avail(self, other):
        if self.kind == LocalTypeKinds.NULLTYPE and other.kind == LocalTypeKinds.NULLTYPE:
            return True
        if (self.kind == LocalTypeKinds.INTCHOICE and other.kind == LocalTypeKinds.INTCHOICE) \
           or (self.kind == LocalTypeKinds.EXTCHOICE and other.kind == LocalTypeKinds.EXTCHOICE):
            msg_evs_s = set(self.options.keys())
            msg_evs_o = set(other.options.keys())
            if not msg_evs_s == msg_evs_o:
                return False
            else:
                for msg_ev in msg_evs_s:
                    if not self.options[msg_ev].congruent_wo_avail(other.options[msg_ev]):
                        return False
                    return True
        elif self.kind == LocalTypeKinds.RECURSION and other.kind == LocalTypeKinds.RECURSION:
            other.subst_var(other.bound_variable, self.bound_variable)
            return self.continuation.congruent_wo_avail(other.continuation)
        elif self.kind == LocalTypeKinds.REC_VAR and other.kind == LocalTypeKinds.REC_VAR:
            return self.ref_variable == self.ref_variable
        else:
            return False

    def remove_avail_ann(self):
        # self.avail = None
        self.lazy_avail = None
        if self.kind == LocalTypeKinds.NULLTYPE:
            pass
        elif self.kind == LocalTypeKinds.INTCHOICE or self.kind == LocalTypeKinds.EXTCHOICE:
            for cont in self.options.values():
                cont.remove_avail_ann()
        elif self.kind == LocalTypeKinds.RECURSION:
            self.continuation.remove_avail_ann()
        elif self.kind == LocalTypeKinds.REC_VAR:
            pass
        else:
            raise Exception('Kind of local type not specified properly.')

    @staticmethod
    def merge(list_to_merge, process):
        filtered_list_to_merge = list(filter(lambda l: l.kind != LocalTypeKinds.IGNORE, list_to_merge))
        if len(filtered_list_to_merge) == 0:
            return LocalType(LocalTypeKinds.IGNORE, None, None)
        current_local_type = filtered_list_to_merge[0]
        for i in range(1, len(filtered_list_to_merge)):
            current_local_type = LocalType.merge_two(current_local_type, filtered_list_to_merge[i], process)
        return current_local_type

    @staticmethod
    def merge_two(local_type_1, local_type_2, process):
        # we use merged_conts.avail sometimes twice here somehow but should not matter
        # this test includes the equality of message sets (projected onto process already)
        if local_type_1.congruent_wo_avail(local_type_2):
            # local_type_1.avail.update(local_type_2.avail)
            # return local_type_1
            # return union of both availability message sets
            new_availability = UnionAvailabilitySet([local_type_1.lazy_avail, local_type_2.lazy_avail])
            local_type_1.lazy_avail = new_availability
            return local_type_1
        elif local_type_1.kind == LocalTypeKinds.INTCHOICE and local_type_2.kind == LocalTypeKinds.INTCHOICE:
            if local_type_1.options.keys() == local_type_2.options.keys():
                # we know that they agree on message send events
                new_options = []
                for msg_snd_ev in local_type_1.options.keys():
                    merged_cont = LocalType.merge_two(local_type_1.options[msg_snd_ev], local_type_2.options[msg_snd_ev], process)
                    new_options.append((msg_snd_ev, merged_cont))
                return LocalType(LocalTypeKinds.INTCHOICE, new_options, # local_type_1.avail.union(local_type_2.avail),
                                 UnionAvailabilitySet([local_type_1.lazy_avail, local_type_2.lazy_avail]))
            else:
                raise ProjectionUndefined('Not the same send options to merge')
        elif local_type_1.kind == LocalTypeKinds.EXTCHOICE and local_type_2.kind == LocalTypeKinds.EXTCHOICE:
            # first, we compute the different set of options
            msg_send_evs_1 = set(local_type_1.options.keys())
            msg_send_evs_2 = set(local_type_2.options.keys())
            msg_send_evs_only_1 = msg_send_evs_1.difference(msg_send_evs_2)
            msg_send_evs_only_2 = msg_send_evs_2.difference(msg_send_evs_1)
            msg_send_evs_common = msg_send_evs_1.intersection(msg_send_evs_2)
            new_options = []
            # check whether we need to check availability
            some_sender = next(iter(local_type_1.options.keys())).sender
            no_availability_check_needed = (
                len(local_type_1.options) == len(list(filter(lambda k: k.sender == some_sender, local_type_1.options.keys())))
                and
                len(local_type_2.options) == len(list(filter(lambda k: k.sender == some_sender, local_type_2.options.keys())))
            )
            # assert local_type_1.avail == local_type_1.lazy_avail.compute_avail_msgs()
            # assert local_type_2.avail == local_type_2.lazy_avail.compute_avail_msgs()
            # 1 : only in 1
            for msg_snd_ev in msg_send_evs_only_1:
                # check conditions for merge
                if no_availability_check_needed or \
                        (msg_snd_ev not in local_type_2.lazy_avail.compute_avail_msgs() and
                         msg_snd_ev not in msg_send_evs_only_2):
                    new_options.append((msg_snd_ev, local_type_1.options[msg_snd_ev]))
                else:
                    raise ProjectionUndefined('Reception event was not unique in branches')
            # 2 : only in 2
            for msg_snd_ev in msg_send_evs_only_2:
                if no_availability_check_needed or \
                        (msg_snd_ev not in local_type_1.lazy_avail.compute_avail_msgs()
                         and msg_snd_ev not in msg_send_evs_only_1):
                    new_options.append((msg_snd_ev, local_type_2.options[msg_snd_ev]))
                else:
                    raise ProjectionUndefined('Reception event was not unique in branches')
            # 3 : common
            for msg_snd_ev in msg_send_evs_common:
                merged_cont = LocalType.merge_two(local_type_1.options[msg_snd_ev], local_type_2.options[msg_snd_ev],
                                              process)
                new_options.append((msg_snd_ev, merged_cont))
            return LocalType(LocalTypeKinds.EXTCHOICE, new_options, # local_type_1.avail.union(local_type_2.avail),
                             UnionAvailabilitySet([local_type_1.lazy_avail, local_type_2.lazy_avail]))
        elif local_type_1.kind == LocalTypeKinds.NULLTYPE or local_type_2.kind == LocalTypeKinds.NULLTYPE:
            raise ProjectionUndefined('Merge 0 with non-0 continuation; impossible in all MST due to syntactic choices')
        else:
            raise ProjectionUndefined

    def get_size(self):
        if self.kind == LocalTypeKinds.NULLTYPE:
            return 1
        elif self.kind == LocalTypeKinds.EXTCHOICE or self.kind == LocalTypeKinds.INTCHOICE:
            res = len(self.options)
            for continuation in self.options.values():
                res += continuation.get_size()
            return res
        elif self.kind == LocalTypeKinds.RECURSION:
            return 1 + self.continuation.get_size()
        elif self.kind == LocalTypeKinds.REC_VAR:
            return 1


class LocalTypeKinds(Enum):
    NULLTYPE = 'n'
    INTCHOICE = 'i'
    EXTCHOICE = 'e'
    RECURSION = 'r'
    REC_VAR = 'v'
    IGNORE = 'g'