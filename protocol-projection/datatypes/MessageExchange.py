from datatypes.MessageSndRcv import *


# defines a class for a message exchange: sender -> receiver : message
class MessageExchange:

    def __init__(self, sender, receiver, message):
        # all represented as strings
        self.sender = sender
        self.receiver = receiver
        self.message = message

    def __str__(self):
        return self.sender + ' -> ' + self.receiver + ' : ' + self.message

    def __eq__(self, other):
        return self.sender == other.sender and self.receiver == other.receiver and self.message == other.message

    # returns the two processes involved as set
    def get_procs(self):
        return {self.sender, self.receiver}

    # applies projection of a MessageExchange object onto a process, yielding an object of type MessageSndRcv
    def project_onto(self, process):
        if process == self.sender:
            return MessageSndRcv(MessageSndRcvKinds.SND, self.sender, self.receiver, self.message)
        elif process == self.receiver:
            return MessageSndRcv(MessageSndRcvKinds.RCV, self.sender, self.receiver, self.message)
        else: # neither sender nor receiver
            return MessageSndRcvEmpty()


class MessageExchangeEmpty:

    # defines an empty message exchange to be able to keep track of those when projecting
    def __init__(self):
        pass

    def __str__(self):
        return "epsilon"

    def project_onto(self, _process):
        return MessageSndRcvEmpty()
