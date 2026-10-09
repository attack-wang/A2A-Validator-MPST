from datatypes.classical_projection.LocalType import LocalTypeKinds
from collections import defaultdict


class TopLocalType:

    def __init__(self, local_type, msg_map):
        self.local_type = local_type
        # remove the annotations of available messages for hashing etc.
        self.local_type.remove_avail_ann()
        # we assert that all variable binders are unique
        if not self.has_unique_binders():
            raise Exception("Binders are not unique!")
        self.rec_var_map = self.compute_rec_var_map()
        self.state_map = defaultdict(lambda: "No")
        self.msg_map = msg_map

    def __str__(self):
        return str(self.local_type)

    def has_unique_binders(self):
        if self.local_type.set_of_unique_binders() is None:
            return False
        else:
            return True

    def compute_rec_var_map(self):
        assert self.has_unique_binders()
        result = self.local_type.compute_rec_var_map()
        return dict(result)

    def get_spin_repr(self):
        # this prints a label for everything, see whether it simply starts with the first then
        list_unprocessed_subterms = [self.local_type]
        res_str = ''
        while len(list_unprocessed_subterms) != 0:
            curr_subterm = list_unprocessed_subterms.pop()
            # we check whether it has been already processed before pushing it there
            # get the label and print it
            _, label = self.get_state_for(curr_subterm)
            res_str += label + ':\n'
            # CA on which type of local type it is
            if curr_subterm.kind == LocalTypeKinds.NULLTYPE:
                res_str += '\tskip\n'
            elif curr_subterm.kind == LocalTypeKinds.INTCHOICE or curr_subterm.kind == LocalTypeKinds.EXTCHOICE:
                res_str += '\tif\n'
                helper_list_for_order = []
                for opt_msx in curr_subterm.options.keys():
                    msx_cond = opt_msx.get_spin_repr(self.msg_map)
                    existed, label_cont = self.get_state_for(curr_subterm.options[opt_msx])
                    res_str += '\t:: ' + msx_cond + ' -> goto ' + label_cont + '\n'
                    if not existed:
                        helper_list_for_order.append(curr_subterm.options[opt_msx])
                list_unprocessed_subterms.extend(reversed(helper_list_for_order))
                res_str += '\tfi\n'
            elif curr_subterm.kind == LocalTypeKinds.RECURSION:
                existed, label_cont = self.get_state_for(curr_subterm.continuation)
                res_str += '\tgoto ' + label_cont + '\n'
                if not existed:
                    list_unprocessed_subterms.append(curr_subterm.continuation)
            elif curr_subterm.kind == LocalTypeKinds.REC_VAR:
                cont = self.rec_var_map[curr_subterm.ref_variable]
                existed, label_cont = self.get_state_for(cont)
                assert existed
                res_str += '\tgoto ' + label_cont + '\n'
            else:
                raise Exception('Kind of local type is bad.')
        return res_str

    def get_state_for(self, subterm):
        existed = True
        if self.state_map[subterm] == "No":
            # not present yet, get it as new one
            self.state_map[subterm] = "state" + str(len(self.state_map))
            existed = False
        return (existed, self.state_map[subterm])
