'''
Deprecated compatibility shim: the QuestionBank implementation now lives in
question_bank.py, which is the module name imported by quiz_cli.py. This
module simply re-exports the real classes so any legacy
"from questionbank import ..." statements keep working, while eliminating the
duplicate/conflicting implementation that previously caused the SyntaxError.
This file may be safely deleted; nothing in the project imports it.
'''
from question_bank import QuestionBank, QuestionBankError  # noqa: F401