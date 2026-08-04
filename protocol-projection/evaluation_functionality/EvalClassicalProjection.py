# EvalClassicalProjection.py

from datatypes.classical_projection.GlobalTypeTop import GlobalTypeTop
from evaluation_functionality.evaluation_config import PREFIX_EVAL_CLASSICAL

# This class provides an API to call the functionalities of classical projection (for the evaluation_functionality)
# as well as the expected results for known examples
class EvalClassicalProjection:

    MAP_EXAMPLE_NAME_EXPECTED_RESULT = {
        "Instr. Contr. Prot. A": True,
        "Instr. Contr. Prot. B": True,
        "Multi Party Game": True,
        "OAuth2": True,
        "Streaming": True,
        "Non-Compatible Merge": True,
        "Spring-Hibernate": True,
        "Group Present": True,
        "Late Learning": True,
        "Load Balancer (n=10)": True,
        "Logging (n=10)": True,
        "2 Buyer Prot.": True,
        "2B-Prot. - Omit No": False,
        "2B-Prot. - Subscription": False,
        "2B-Prot. - Inner Rec.": True,
        "Odd-Even": False,
        "Motivation RCV Violated (Gr)": False,
        "Motivation RCV Satisfied (Gr')": True,
        "Motivation SND Violated (Gs)": False,
        "Motivation SND Satisfied (Gs')": True,
        "Example Folded (Gfold)": False,
        "Example Unfolded (Gunf)": True
    }

    def __init__(self, global_type, example_name=None):
        self.top_global_type = GlobalTypeTop(global_type)
        self.example_name = example_name

    @staticmethod
    # returns the prefix where to store the evaluation data
    def get_eval_data_path_prefix():
        return PREFIX_EVAL_CLASSICAL

    # returns the expected result for the given example if provided
    def get_expected_result(self):
        assert self.example_name is not None
        return EvalClassicalProjection.MAP_EXAMPLE_NAME_EXPECTED_RESULT.get(self.example_name)

    # calls the classical projection operator
    def project_onto(self, proc):
        return self.top_global_type.project_onto(proc)

    # gives the size as global type
    def get_size(self):
        return self.top_global_type.get_size()
