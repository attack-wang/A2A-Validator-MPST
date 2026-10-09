# Generated from /home/fms/git-repos/Session MSC/async-mpst-gen-choice/parser/GlobalType.g4 by ANTLR 4.9
from antlr4 import *
from io import StringIO
import sys
# Python 3.10+ uses typing.TextIO instead of typing.io.TextIO
if sys.version_info >= (3, 10):
    from typing import TextIO
else:
    from typing.io import TextIO



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\21")
        buf.write("X\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\3\2\3\2\3\3\3\3\3\3\3\4\3\4")
        buf.write("\7\4)\n\4\f\4\16\4,\13\4\3\5\3\5\7\5\60\n\5\f\5\16\5\63")
        buf.write("\13\5\3\6\3\6\3\7\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3\n\3\13")
        buf.write("\3\13\3\f\3\f\3\r\3\r\3\16\3\16\3\17\6\17I\n\17\r\17\16")
        buf.write("\17J\3\17\3\17\3\20\3\20\3\20\3\20\6\20S\n\20\r\20\16")
        buf.write("\20T\3\20\3\20\2\2\21\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21")
        buf.write("\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21\3\2\7\3\2c")
        buf.write("|\5\2\62;C\\c|\3\2C\\\5\2\13\f\17\17\"\"\4\2\f\f\17\17")
        buf.write("\2[\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2")
        buf.write("\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23")
        buf.write("\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3")
        buf.write("\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\3!\3\2\2\2\5#\3\2\2\2")
        buf.write("\7&\3\2\2\2\t-\3\2\2\2\13\64\3\2\2\2\r\66\3\2\2\2\179")
        buf.write("\3\2\2\2\21;\3\2\2\2\23=\3\2\2\2\25?\3\2\2\2\27A\3\2\2")
        buf.write("\2\31C\3\2\2\2\33E\3\2\2\2\35H\3\2\2\2\37N\3\2\2\2!\"")
        buf.write("\7\u03be\2\2\"\4\3\2\2\2#$\7o\2\2$%\7w\2\2%\6\3\2\2\2")
        buf.write("&*\t\2\2\2\')\t\3\2\2(\'\3\2\2\2),\3\2\2\2*(\3\2\2\2*")
        buf.write("+\3\2\2\2+\b\3\2\2\2,*\3\2\2\2-\61\t\4\2\2.\60\t\3\2\2")
        buf.write("/.\3\2\2\2\60\63\3\2\2\2\61/\3\2\2\2\61\62\3\2\2\2\62")
        buf.write("\n\3\2\2\2\63\61\3\2\2\2\64\65\7\62\2\2\65\f\3\2\2\2\66")
        buf.write("\67\7/\2\2\678\7@\2\28\16\3\2\2\29:\7*\2\2:\20\3\2\2\2")
        buf.write(";<\7+\2\2<\22\3\2\2\2=>\7.\2\2>\24\3\2\2\2?@\7\60\2\2")
        buf.write("@\26\3\2\2\2AB\7=\2\2B\30\3\2\2\2CD\7<\2\2D\32\3\2\2\2")
        buf.write("EF\7-\2\2F\34\3\2\2\2GI\t\5\2\2HG\3\2\2\2IJ\3\2\2\2JH")
        buf.write("\3\2\2\2JK\3\2\2\2KL\3\2\2\2LM\b\17\2\2M\36\3\2\2\2NO")
        buf.write("\7\61\2\2OP\7\61\2\2PR\3\2\2\2QS\n\6\2\2RQ\3\2\2\2ST\3")
        buf.write("\2\2\2TR\3\2\2\2TU\3\2\2\2UV\3\2\2\2VW\b\20\2\2W \3\2")
        buf.write("\2\2\7\2*\61JT\3\b\2\2")
        return buf.getvalue()


class GlobalTypeLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    RECURSION = 1
    MU = 2
    LOWCASESTART = 3
    UPPCASESTART = 4
    ZERO = 5
    ARROW = 6
    PAROP = 7
    PARCL = 8
    COMMA = 9
    DOT = 10
    SEM = 11
    COLON = 12
    CHOICE = 13
    WS = 14
    COMMENTS = 15

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'\u03BC'", "'mu'", "'0'", "'->'", "'('", "')'", "','", "'.'", 
            "';'", "':'", "'+'" ]

    symbolicNames = [ "<INVALID>",
            "RECURSION", "MU", "LOWCASESTART", "UPPCASESTART", "ZERO", "ARROW", 
            "PAROP", "PARCL", "COMMA", "DOT", "SEM", "COLON", "CHOICE", 
            "WS", "COMMENTS" ]

    ruleNames = [ "RECURSION", "MU", "LOWCASESTART", "UPPCASESTART", "ZERO", 
                  "ARROW", "PAROP", "PARCL", "COMMA", "DOT", "SEM", "COLON", 
                  "CHOICE", "WS", "COMMENTS" ]

    grammarFileName = "GlobalType.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


