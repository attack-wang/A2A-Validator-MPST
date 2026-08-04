from parsing.GlobalTypeLexer import *
from parsing.GlobalTypeParser import *
from parsing.Listener import *
from datatypes.classical_projection.GlobalTypeTop import *

# parses a global type from a file into object of type 'GlobalTypeParsed'
def get_gt_from_file(file_name):
    return get_input_from_file(file_name)

# parses a global type from a file into object and obtains one of type 'GlobalTypeTOP'
def get_tplv_gt_from_file(file_name):
    return GlobalTypeTop(get_gt_from_file(file_name))

### internal

def get_input_from_file(file_name):
    f = open(file_name)
    to_parse = InputStream(f.read())
    return parse_input(to_parse)

def parse_input(input):
    lexer = GlobalTypeLexer(input)
    stream = CommonTokenStream(lexer)
    parser = GlobalTypeParser(stream)
    tree = parser.spec()
    listener = Listener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    assert len(listener.stack) == 1
    return listener.stack[0]
