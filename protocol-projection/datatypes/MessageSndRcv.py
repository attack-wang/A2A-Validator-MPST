from enum import Enum


# defines a class for message send and receive events for a particular process: sender ? message; receiver ! message
class MessageSndRcv:

    def __init__(self, kind, sender, receiver, message):
        # kind specifies whether it is a send or receive event
        self.kind = kind
        # all represented as strings
        self.sender = sender
        self.receiver = receiver
        self.message = message

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __hash__(self):
        return hash(self.kind) + (hash(self.sender) * hash(self.receiver) * hash(self.message))

    def __str__(self):
        if self.kind == MessageSndRcvKinds.SND:
            return self.receiver + '!' + self.message
        else:
            return self.sender + '?' + self.message

    # computes the spin representation
    def get_spin_repr(self, msg_map):
        prefix = self.sender + '_' + self.receiver + self.kind.value
        if msg_map[self.message] == -1:
            msg_map[self.message] = len(msg_map)
        msg = str(msg_map[self.message])
        return prefix + msg

    @staticmethod
    def set_project_onto(process, set_of_events):
        return set(filter(lambda me: process == me.sender or process == me.receiver, set_of_events))


# specifies the different kind of message events
class MessageSndRcvKinds(Enum):
    SND = '!'
    RCV = '?'

# as for the MessageExchange, we define an empty version
class MessageSndRcvEmpty:

    def __init__(self):
        pass

    def __str__(self):
        return "epsilon"
