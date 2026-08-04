from parsing.GlobalTypeListener import GlobalTypeListener
from datatypes.GlobalTypeParsed import *
from datatypes.MessageExchange import *


class Listener(GlobalTypeListener):
    def __init__(self):
        # use self.globaltype here as return address
        self.stack = []
        # self.mult_options_count = 0

    # global type

    def enterGlobaltype(self, ctx):
        pass

    def exitGlobaltype(self, ctx):
        pass

    # null type

    def exitNull_type(self, ctx):
        self.stack.append(GlobalTypeParsed(GlobalTypeKinds.NULLTYPE, False))

    # choice message exchanges
    # similar to parallels

    def enterChoice_msg_exc(self, ctx):
        # self.mult_options_count += 1
        self.stack.append(StackMarker.CHOICE)

    def exitChoice_msg_exc(self, ctx):
        options = []
        temp = self.stack.pop()
        while temp != StackMarker.CHOICE:
            # should be pairs of msg_exc and continuation
            options.append(temp.options[0])
            temp = self.stack.pop()
        options.reverse()
        choice = GlobalTypeParsed(GlobalTypeKinds.CHOICE, options)
        self.stack.append(choice)
        # self.mult_options_count -= 1
        # assert self.mult_options_count >= 0

    def exitSingle_choice(self, ctx):
        cont = self.stack.pop()
        msg_exc = self.stack.pop()
        choice = GlobalTypeParsed(GlobalTypeKinds.CHOICE, [(msg_exc, cont)])
    # if self.mult_options_count != 0:
    #     self.stack.append((msg_exc, cont))
    # else:
        self.stack.append(choice)

    # Messages, similar to message exchange
    def exitMsg_exchange(self, ctx):
        msg = self.stack.pop()
        proc2 = self.stack.pop()
        proc1 = self.stack.pop()
        self.stack.append(MessageExchange(proc1, proc2, msg))

    def exitProc(self, ctx):
        self.stack.append(ctx.getText())

    def exitMsg(self, ctx):
        self.stack.append(ctx.getText())

    # Recursion
    def exitRecursion(self, ctx):
        cont = self.stack.pop()
        var = self.stack.pop()
        self.stack.append(GlobalTypeParsed(GlobalTypeKinds.RECURSION, (var, cont)))

    def exitBind_rec_variable(self, ctx):
        self.stack.append(ctx.getText())

    def exitRef_rec_variable(self, ctx):
        var = ctx.getText()
        self.stack.append(GlobalTypeParsed(GlobalTypeKinds.REC_VAR, var))


class StackMarker(Enum):
    CHOICE = '0'


