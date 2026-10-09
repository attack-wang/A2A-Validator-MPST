# Generated from /home/fms/git-repos/Session MSC/async-mpst-gen-choice/parser/GlobalType.g4 by ANTLR 4.9
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GlobalTypeParser import GlobalTypeParser
else:
    from GlobalTypeParser import GlobalTypeParser

# This class defines a complete generic visitor for a parse tree produced by GlobalTypeParser.

class GlobalTypeVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by GlobalTypeParser#spec.
    def visitSpec(self, ctx:GlobalTypeParser.SpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GlobalTypeParser#globaltype.
    def visitGlobaltype(self, ctx:GlobalTypeParser.GlobaltypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GlobalTypeParser#null_type.
    def visitNull_type(self, ctx:GlobalTypeParser.Null_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GlobalTypeParser#choice_msg_exc.
    def visitChoice_msg_exc(self, ctx:GlobalTypeParser.Choice_msg_excContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GlobalTypeParser#single_choice.
    def visitSingle_choice(self, ctx:GlobalTypeParser.Single_choiceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GlobalTypeParser#msg_exchange.
    def visitMsg_exchange(self, ctx:GlobalTypeParser.Msg_exchangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GlobalTypeParser#recursion.
    def visitRecursion(self, ctx:GlobalTypeParser.RecursionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GlobalTypeParser#bind_rec_variable.
    def visitBind_rec_variable(self, ctx:GlobalTypeParser.Bind_rec_variableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GlobalTypeParser#ref_rec_variable.
    def visitRef_rec_variable(self, ctx:GlobalTypeParser.Ref_rec_variableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GlobalTypeParser#proc.
    def visitProc(self, ctx:GlobalTypeParser.ProcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GlobalTypeParser#msg.
    def visitMsg(self, ctx:GlobalTypeParser.MsgContext):
        return self.visitChildren(ctx)



del GlobalTypeParser