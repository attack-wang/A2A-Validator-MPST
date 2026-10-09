from parsing.GlobalTypeLexer import *
from parsing.GlobalTypeParser import *
from parsing.Listener import *
from datatypes.classical_projection.GlobalTypeTop import *
from antlr4.error.ErrorListener import ErrorListener


class _StrictErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise ValueError(f"Protocol syntax error at {line}:{column}: {msg}")

# parses a global type from a file into object of type 'GlobalTypeParsed'
def get_gt_from_file(file_name):
    return get_input_from_file(file_name)

# parses a global type from a file into object and obtains one of type 'GlobalTypeTOP'
def get_tplv_gt_from_file(file_name):
    return GlobalTypeTop(get_gt_from_file(file_name))

### internal

def get_input_from_file(file_name):
    with open(file_name, encoding="utf-8") as f:
        to_parse = InputStream(f.read())
    return parse_input(to_parse)

def parse_input(input):
    lexer = GlobalTypeLexer(input)
    lexer.removeErrorListeners()
    lexer.addErrorListener(_StrictErrorListener())
    stream = CommonTokenStream(lexer)
    parser = GlobalTypeParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(_StrictErrorListener())
    tree = parser.spec()
    listener = Listener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    assert len(listener.stack) == 1
    return listener.stack[0]
