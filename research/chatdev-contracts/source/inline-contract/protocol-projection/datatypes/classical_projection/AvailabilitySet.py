from datatypes.GlobalTypeParsed import *
from datatypes.classical_projection.LocalType import *
import os


class AvailabilitySet:
    def __init__(self, global_type, process, blocked_procs, handled_vars, rec_var_map, vars_empty):
        self.isoption = type(global_type) is tuple
        self.option = global_type
        self.global_type = global_type
        self.process = process
        self.blocked_procs = blocked_procs
        self.handled_vars = handled_vars
        self.rec_var_map = rec_var_map
        self.vars_empty = vars_empty

    def compute_avail_msgs(self):
        avail_check = os.getenv('AVAIL_CHECK')
        if avail_check == "FALSE":
            return set()
        if self.isoption:
            avail_msgs_option = self.option[1].avail_msgs(self.process, {self.process}, set(), self.rec_var_map)
            # we have to play this trick here to filter the FIFO-ordered messages b/c
            # the msg_exc is not present in the computation of avail_msgs_option
            avail_msgs_option_possible = set(filter(lambda m:
                                                    m.sender != self.option[0].sender or
                                                    m.receiver != self.option[0].receiver,
                                                    avail_msgs_option))
            return avail_msgs_option_possible
        elif self.global_type.kind == GlobalTypeKinds.NULLTYPE:
            return set()
        elif self.global_type.kind == GlobalTypeKinds.CHOICE:
            # 1) Process is sender
            if self.global_type.options[0][0].sender == self.process:
                avail_set = set()
                for option in self.global_type.options:
                    avail_set_udp = option[1].avail_msgs(self.process, {option[0].sender, option[0].receiver}, set(), self.rec_var_map)
                    avail_set.update(avail_set_udp)
                return avail_set
            # 2) now, self.process can either not be part of exchange or the receiver
            else:
                # sort continuations where self.process is part of msg exchange (as receiver) or not
                list_part_of_msg_exc = list(filter(lambda o: o[0].receiver == self.process, self.global_type.options))
                fst_avail_msgs = set()
                if len(list_part_of_msg_exc) > 0:
                    # COMPUTE AVAIL
                    for option in list_part_of_msg_exc:
                        # USE AVAIL
                        avail_msgs_option = option[1].avail_msgs(self.process, {self.process}, set(), self.rec_var_map)
                        # we have to play this trick here to filter the FIFO-ordered messages b/c
                        # the msg_exc is not present in the computation of avail_msgs_option
                        avail_msgs_option_possible = set(filter(lambda m:
                                                                m.sender != option[0].sender or
                                                                m.receiver != option[0].receiver,
                                                                avail_msgs_option))
                        fst_avail_msgs.update(avail_msgs_option_possible)
                list_not_part_of_msg_exc = list(filter(lambda o: o[0].receiver != self.process, self.global_type.options))
                snd_avail_msgs = set()
                for option in list_not_part_of_msg_exc:
                    # not part of msg_exc so we omit to project to an empty one here
                    proj_cont = option[1].project_onto(self.process, self.vars_empty, self.rec_var_map)
                    # check whether the continuation is
                    is_rec_for_one = False
                    for rec_var in self.vars_empty:
                        if proj_cont.kind == LocalTypeKinds.REC_VAR and proj_cont.ref_variable == rec_var:
                            is_rec_for_one = True
                            break
                    if not is_rec_for_one:
                        snd_avail_msgs.update(proj_cont.avail)
                return fst_avail_msgs.union(snd_avail_msgs)
        elif self.global_type.kind == GlobalTypeKinds.RECURSION:
            proj_cont = self.global_type.continuation.project_onto(self.process, {self.global_type.bound_variable}.union(self.vars_empty), self.rec_var_map)
            is_bound_variable_itself = proj_cont.kind == LocalTypeKinds.REC_VAR and \
                                       proj_cont.ref_variable == self.global_type.bound_variable
            bound_variable_occurs = proj_cont.rec_var_occurs(self.global_type.bound_variable)
            if (not is_bound_variable_itself and bound_variable_occurs) or not bound_variable_occurs:
                avail_msgs = self.global_type.continuation.avail_msgs(self.process, {self.process}, {self.global_type.bound_variable}, self.rec_var_map)
                return avail_msgs
            else:
                return set()
        elif self.global_type.kind == GlobalTypeKinds.REC_VAR:
            avail_msgs = self.rec_var_map[self.global_type.ref_variable].avail_msgs(self.process, {self.process}, {self.global_type.ref_variable}, self.rec_var_map)
            return avail_msgs
        else:
            raise Exception('how did we get here?')
