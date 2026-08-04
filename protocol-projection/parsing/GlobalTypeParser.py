# Generated from /home/fms/git-repos/Session MSC/async-mpst-gen-choice/parser/GlobalType.g4 by ANTLR 4.9
# encoding: utf-8
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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\21")
        buf.write("G\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\3\2\3\2\3\2\3\3")
        buf.write("\3\3\3\3\3\3\3\3\3\3\3\3\3\3\5\3$\n\3\3\4\3\4\3\5\3\5")
        buf.write("\3\5\7\5+\n\5\f\5\16\5.\13\5\3\6\3\6\3\6\3\6\3\7\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\b\3\t\3\t\3\n\3\n\3\13")
        buf.write("\3\13\3\f\3\f\3\f\2\2\r\2\4\6\b\n\f\16\20\22\24\26\2\3")
        buf.write("\3\2\3\4\2@\2\30\3\2\2\2\4#\3\2\2\2\6%\3\2\2\2\b\'\3\2")
        buf.write("\2\2\n/\3\2\2\2\f\63\3\2\2\2\169\3\2\2\2\20>\3\2\2\2\22")
        buf.write("@\3\2\2\2\24B\3\2\2\2\26D\3\2\2\2\30\31\5\4\3\2\31\32")
        buf.write("\7\2\2\3\32\3\3\2\2\2\33$\5\6\4\2\34$\5\n\6\2\35\36\7")
        buf.write("\t\2\2\36\37\5\b\5\2\37 \7\n\2\2 $\3\2\2\2!$\5\16\b\2")
        buf.write("\"$\5\22\n\2#\33\3\2\2\2#\34\3\2\2\2#\35\3\2\2\2#!\3\2")
        buf.write("\2\2#\"\3\2\2\2$\5\3\2\2\2%&\7\7\2\2&\7\3\2\2\2\',\5\n")
        buf.write("\6\2()\7\17\2\2)+\5\n\6\2*(\3\2\2\2+.\3\2\2\2,*\3\2\2")
        buf.write("\2,-\3\2\2\2-\t\3\2\2\2.,\3\2\2\2/\60\5\f\7\2\60\61\7")
        buf.write("\f\2\2\61\62\5\4\3\2\62\13\3\2\2\2\63\64\5\24\13\2\64")
        buf.write("\65\7\b\2\2\65\66\5\24\13\2\66\67\7\16\2\2\678\5\26\f")
        buf.write("\28\r\3\2\2\29:\t\2\2\2:;\5\20\t\2;<\7\f\2\2<=\5\4\3\2")
        buf.write("=\17\3\2\2\2>?\7\5\2\2?\21\3\2\2\2@A\7\5\2\2A\23\3\2\2")
        buf.write("\2BC\7\6\2\2C\25\3\2\2\2DE\7\5\2\2E\27\3\2\2\2\4#,")
        return buf.getvalue()


class GlobalTypeParser ( Parser ):

    grammarFileName = "GlobalType.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'\u03BC'", "'mu'", "<INVALID>", "<INVALID>", 
                     "'0'", "'->'", "'('", "')'", "','", "'.'", "';'", "':'", 
                     "'+'" ]

    symbolicNames = [ "<INVALID>", "RECURSION", "MU", "LOWCASESTART", "UPPCASESTART", 
                      "ZERO", "ARROW", "PAROP", "PARCL", "COMMA", "DOT", 
                      "SEM", "COLON", "CHOICE", "WS", "COMMENTS" ]

    RULE_spec = 0
    RULE_globaltype = 1
    RULE_null_type = 2
    RULE_choice_msg_exc = 3
    RULE_single_choice = 4
    RULE_msg_exchange = 5
    RULE_recursion = 6
    RULE_bind_rec_variable = 7
    RULE_ref_rec_variable = 8
    RULE_proc = 9
    RULE_msg = 10

    ruleNames =  [ "spec", "globaltype", "null_type", "choice_msg_exc", 
                   "single_choice", "msg_exchange", "recursion", "bind_rec_variable", 
                   "ref_rec_variable", "proc", "msg" ]

    EOF = Token.EOF
    RECURSION=1
    MU=2
    LOWCASESTART=3
    UPPCASESTART=4
    ZERO=5
    ARROW=6
    PAROP=7
    PARCL=8
    COMMA=9
    DOT=10
    SEM=11
    COLON=12
    CHOICE=13
    WS=14
    COMMENTS=15

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class SpecContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def globaltype(self):
            return self.getTypedRuleContext(GlobalTypeParser.GlobaltypeContext,0)


        def EOF(self):
            return self.getToken(GlobalTypeParser.EOF, 0)

        def getRuleIndex(self):
            return GlobalTypeParser.RULE_spec

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSpec" ):
                listener.enterSpec(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSpec" ):
                listener.exitSpec(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSpec" ):
                return visitor.visitSpec(self)
            else:
                return visitor.visitChildren(self)




    def spec(self):

        localctx = GlobalTypeParser.SpecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_spec)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 22
            self.globaltype()
            self.state = 23
            self.match(GlobalTypeParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GlobaltypeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def null_type(self):
            return self.getTypedRuleContext(GlobalTypeParser.Null_typeContext,0)


        def single_choice(self):
            return self.getTypedRuleContext(GlobalTypeParser.Single_choiceContext,0)


        def PAROP(self):
            return self.getToken(GlobalTypeParser.PAROP, 0)

        def choice_msg_exc(self):
            return self.getTypedRuleContext(GlobalTypeParser.Choice_msg_excContext,0)


        def PARCL(self):
            return self.getToken(GlobalTypeParser.PARCL, 0)

        def recursion(self):
            return self.getTypedRuleContext(GlobalTypeParser.RecursionContext,0)


        def ref_rec_variable(self):
            return self.getTypedRuleContext(GlobalTypeParser.Ref_rec_variableContext,0)


        def getRuleIndex(self):
            return GlobalTypeParser.RULE_globaltype

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGlobaltype" ):
                listener.enterGlobaltype(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGlobaltype" ):
                listener.exitGlobaltype(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGlobaltype" ):
                return visitor.visitGlobaltype(self)
            else:
                return visitor.visitChildren(self)




    def globaltype(self):

        localctx = GlobalTypeParser.GlobaltypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_globaltype)
        try:
            self.state = 33
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [GlobalTypeParser.ZERO]:
                self.enterOuterAlt(localctx, 1)
                self.state = 25
                self.null_type()
                pass
            elif token in [GlobalTypeParser.UPPCASESTART]:
                self.enterOuterAlt(localctx, 2)
                self.state = 26
                self.single_choice()
                pass
            elif token in [GlobalTypeParser.PAROP]:
                self.enterOuterAlt(localctx, 3)
                self.state = 27
                self.match(GlobalTypeParser.PAROP)
                self.state = 28
                self.choice_msg_exc()
                self.state = 29
                self.match(GlobalTypeParser.PARCL)
                pass
            elif token in [GlobalTypeParser.RECURSION, GlobalTypeParser.MU]:
                self.enterOuterAlt(localctx, 4)
                self.state = 31
                self.recursion()
                pass
            elif token in [GlobalTypeParser.LOWCASESTART]:
                self.enterOuterAlt(localctx, 5)
                self.state = 32
                self.ref_rec_variable()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Null_typeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ZERO(self):
            return self.getToken(GlobalTypeParser.ZERO, 0)

        def getRuleIndex(self):
            return GlobalTypeParser.RULE_null_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNull_type" ):
                listener.enterNull_type(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNull_type" ):
                listener.exitNull_type(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNull_type" ):
                return visitor.visitNull_type(self)
            else:
                return visitor.visitChildren(self)




    def null_type(self):

        localctx = GlobalTypeParser.Null_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_null_type)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            self.match(GlobalTypeParser.ZERO)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Choice_msg_excContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def single_choice(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GlobalTypeParser.Single_choiceContext)
            else:
                return self.getTypedRuleContext(GlobalTypeParser.Single_choiceContext,i)


        def CHOICE(self, i:int=None):
            if i is None:
                return self.getTokens(GlobalTypeParser.CHOICE)
            else:
                return self.getToken(GlobalTypeParser.CHOICE, i)

        def getRuleIndex(self):
            return GlobalTypeParser.RULE_choice_msg_exc

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterChoice_msg_exc" ):
                listener.enterChoice_msg_exc(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitChoice_msg_exc" ):
                listener.exitChoice_msg_exc(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitChoice_msg_exc" ):
                return visitor.visitChoice_msg_exc(self)
            else:
                return visitor.visitChildren(self)




    def choice_msg_exc(self):

        localctx = GlobalTypeParser.Choice_msg_excContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_choice_msg_exc)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            self.single_choice()
            self.state = 42
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==GlobalTypeParser.CHOICE:
                self.state = 38
                self.match(GlobalTypeParser.CHOICE)
                self.state = 39
                self.single_choice()
                self.state = 44
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Single_choiceContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def msg_exchange(self):
            return self.getTypedRuleContext(GlobalTypeParser.Msg_exchangeContext,0)


        def DOT(self):
            return self.getToken(GlobalTypeParser.DOT, 0)

        def globaltype(self):
            return self.getTypedRuleContext(GlobalTypeParser.GlobaltypeContext,0)


        def getRuleIndex(self):
            return GlobalTypeParser.RULE_single_choice

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSingle_choice" ):
                listener.enterSingle_choice(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSingle_choice" ):
                listener.exitSingle_choice(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSingle_choice" ):
                return visitor.visitSingle_choice(self)
            else:
                return visitor.visitChildren(self)




    def single_choice(self):

        localctx = GlobalTypeParser.Single_choiceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_single_choice)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 45
            self.msg_exchange()
            self.state = 46
            self.match(GlobalTypeParser.DOT)
            self.state = 47
            self.globaltype()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Msg_exchangeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def proc(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GlobalTypeParser.ProcContext)
            else:
                return self.getTypedRuleContext(GlobalTypeParser.ProcContext,i)


        def ARROW(self):
            return self.getToken(GlobalTypeParser.ARROW, 0)

        def COLON(self):
            return self.getToken(GlobalTypeParser.COLON, 0)

        def msg(self):
            return self.getTypedRuleContext(GlobalTypeParser.MsgContext,0)


        def getRuleIndex(self):
            return GlobalTypeParser.RULE_msg_exchange

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMsg_exchange" ):
                listener.enterMsg_exchange(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMsg_exchange" ):
                listener.exitMsg_exchange(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMsg_exchange" ):
                return visitor.visitMsg_exchange(self)
            else:
                return visitor.visitChildren(self)




    def msg_exchange(self):

        localctx = GlobalTypeParser.Msg_exchangeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_msg_exchange)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 49
            self.proc()
            self.state = 50
            self.match(GlobalTypeParser.ARROW)
            self.state = 51
            self.proc()
            self.state = 52
            self.match(GlobalTypeParser.COLON)
            self.state = 53
            self.msg()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RecursionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def bind_rec_variable(self):
            return self.getTypedRuleContext(GlobalTypeParser.Bind_rec_variableContext,0)


        def DOT(self):
            return self.getToken(GlobalTypeParser.DOT, 0)

        def globaltype(self):
            return self.getTypedRuleContext(GlobalTypeParser.GlobaltypeContext,0)


        def RECURSION(self):
            return self.getToken(GlobalTypeParser.RECURSION, 0)

        def MU(self):
            return self.getToken(GlobalTypeParser.MU, 0)

        def getRuleIndex(self):
            return GlobalTypeParser.RULE_recursion

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRecursion" ):
                listener.enterRecursion(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRecursion" ):
                listener.exitRecursion(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRecursion" ):
                return visitor.visitRecursion(self)
            else:
                return visitor.visitChildren(self)




    def recursion(self):

        localctx = GlobalTypeParser.RecursionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_recursion)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 55
            _la = self._input.LA(1)
            if not(_la==GlobalTypeParser.RECURSION or _la==GlobalTypeParser.MU):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 56
            self.bind_rec_variable()
            self.state = 57
            self.match(GlobalTypeParser.DOT)
            self.state = 58
            self.globaltype()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Bind_rec_variableContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LOWCASESTART(self):
            return self.getToken(GlobalTypeParser.LOWCASESTART, 0)

        def getRuleIndex(self):
            return GlobalTypeParser.RULE_bind_rec_variable

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBind_rec_variable" ):
                listener.enterBind_rec_variable(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBind_rec_variable" ):
                listener.exitBind_rec_variable(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBind_rec_variable" ):
                return visitor.visitBind_rec_variable(self)
            else:
                return visitor.visitChildren(self)




    def bind_rec_variable(self):

        localctx = GlobalTypeParser.Bind_rec_variableContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_bind_rec_variable)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 60
            self.match(GlobalTypeParser.LOWCASESTART)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Ref_rec_variableContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LOWCASESTART(self):
            return self.getToken(GlobalTypeParser.LOWCASESTART, 0)

        def getRuleIndex(self):
            return GlobalTypeParser.RULE_ref_rec_variable

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRef_rec_variable" ):
                listener.enterRef_rec_variable(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRef_rec_variable" ):
                listener.exitRef_rec_variable(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRef_rec_variable" ):
                return visitor.visitRef_rec_variable(self)
            else:
                return visitor.visitChildren(self)




    def ref_rec_variable(self):

        localctx = GlobalTypeParser.Ref_rec_variableContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_ref_rec_variable)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            self.match(GlobalTypeParser.LOWCASESTART)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ProcContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def UPPCASESTART(self):
            return self.getToken(GlobalTypeParser.UPPCASESTART, 0)

        def getRuleIndex(self):
            return GlobalTypeParser.RULE_proc

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProc" ):
                listener.enterProc(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProc" ):
                listener.exitProc(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProc" ):
                return visitor.visitProc(self)
            else:
                return visitor.visitChildren(self)




    def proc(self):

        localctx = GlobalTypeParser.ProcContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_proc)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 64
            self.match(GlobalTypeParser.UPPCASESTART)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MsgContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LOWCASESTART(self):
            return self.getToken(GlobalTypeParser.LOWCASESTART, 0)

        def getRuleIndex(self):
            return GlobalTypeParser.RULE_msg

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMsg" ):
                listener.enterMsg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMsg" ):
                listener.exitMsg(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMsg" ):
                return visitor.visitMsg(self)
            else:
                return visitor.visitChildren(self)




    def msg(self):

        localctx = GlobalTypeParser.MsgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_msg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            self.match(GlobalTypeParser.LOWCASESTART)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





