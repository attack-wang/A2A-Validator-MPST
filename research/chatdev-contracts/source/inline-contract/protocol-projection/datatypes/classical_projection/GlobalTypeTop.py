from datatypes.classical_projection.ProjectionUndefined import *
from datatypes.classical_projection.TopLocalType import *


class GlobalTypeTop:

    def __init__(self, global_type):
        self.global_type = global_type
        # we assert that all variable binders are unique
        if not self.has_unique_binders():
            raise Exception("Binders are not unique!")
        self.rec_var_map = self.compute_rec_var_map()
        self.projections = None

    def __str__(self):
        return str(self.global_type)

    def has_unique_binders(self):
        if self.global_type.set_of_unique_binders() is None:
            return False
        else:
            return True

    def compute_rec_var_map(self):
        assert self.has_unique_binders()
        result = self.global_type.compute_rec_var_map()
        return dict(result)

    def get_procs(self):
        return self.global_type.get_procs()

    def get_size(self):
        return self.global_type.get_size()

    def compute_projections(self):
        list_procs = self.get_procs()
        list_projections = []
        for proc in list_procs:
            list_projections.append((proc, self.project_onto(proc)))
        self.projections = dict(list_projections)

    def is_projectable(self):
        if self.projections is None:
            self.compute_projections()
        for proj in self.projections.values():
            if proj is None:
                return False
        return True

    def project_onto(self, process):
        if process not in self.get_procs():
            raise Exception('Tried to project onto process that is not part of global type.')
        try:
            res = self.global_type.project_onto(process, set(), self.rec_var_map)
            if res.is_defined(): # checks if the local type contains any unresolved issues
                return res
            else:
                raise Exception('Undefined is handled via Exceptions so this should not happen!')
        except ProjectionUndefined:
            return None

    def get_channels_for_spin_repr(self):
        res_str = ''
        list_of_procs = self.get_procs()
        channels = self.global_type.get_used_channels()
        for cname in channels:
            res_str += 'chan ' + cname[0] + '_' + cname[1] + ' = [1] of { int };\n'
        return res_str

    def get_spin_init(self):
        res_str = 'init\n{\n'
        res_str += ';\n'.join('\trun ' + proc + '()' for proc in self.get_procs())
        res_str += '\n}\n'
        return res_str

    def write_spin_repr(self, filename):
        # need to ensure projectability_classical outside for no assertion errors
        assert self.is_projectable()
        res_str = self.get_channels_for_spin_repr()
        res_str += '\n'
        res_str += self.get_spin_init()
        msg_map = defaultdict(lambda: -1)
        for proc in self.projections.keys():
            res_str += '\n'
            res_str += self.get_spin_proc_prefix(proc)
            tplv_proj = TopLocalType(self.projections[proc], msg_map)
            res_str += tplv_proj.get_spin_repr()
            # get updated msg_map
            msg_map = tplv_proj.msg_map
            res_str += self.get_spin_proc_postfix(proc)
        file = open(filename, 'w+')
        file.write(res_str)
        file.close()

    @staticmethod
    def get_spin_proc_prefix(proc):
        return 'proctype ' + proc + '()\n{\n'

    @staticmethod
    def get_spin_proc_postfix(proc):
        return '} /* ' + proc + ' */\n'


