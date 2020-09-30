#MAGIC STRINGS
MESSAGE_TO_LEAVE = "quit"
MESSAGE_FOR_CONNECTION = ""
KICK_MSG = "getout"
PROMOTE_ADMIN = "inviteMan"
MUTE_MSG = "shsh"
PRIVATE_MSG_CHAR = '!'
MANAGERS_VIEW_MSG = "view-managers"


class Message(object):
    """
    This class purpose is to create an object from type Message.
    """
    def __init__(self, message, sender):
        self.message = message
        self.sender = sender


class MessageToExit(Message):
    """Class that creates a Message type object that he's meaning is to disconnect from the server."""
    def __init__(self, sender):
        super(MessageToExit, self).__init__(MESSAGE_TO_LEAVE, sender)


class MessageToCheckConnection(Message):
    """Class that creates an object which it purpose is to check a connection."""
    def __init__(self, sender):
        super(MessageToCheckConnection, self).__init__(MESSAGE_FOR_CONNECTION, sender)


class MessageToKickOut(Message):
    """Class that creates a Message type object that points out that a client needs to be kicked"""
    def __init__(self, sender, to_kick):
        super(MessageToKickOut, self).__init__(KICK_MSG, sender)
        self.to_kick = to_kick


class MessageToInviteMan(Message):
    """Class that creates a Message type object that points a promotion for a new admin."""
    def __init__(self, sender, to_invite):
        super(MessageToInviteMan, self).__init__(PROMOTE_ADMIN, sender)
        self.to_invite = to_invite


class MessageToQuiet(Message):
    """Class that creates a Message type object that points that a client that got as a parameter needs to be muted."""
    def __init__(self, sender, to_shsh):
        super(MessageToQuiet, self).__init__(MUTE_MSG, sender)
        self.to_shsh = to_shsh


class PrivateMessage(Message):
    """Class that creates a Message type object that points that a client that got as a parameter needs to be muted."""
    def __init__(self, sender, message, address):
        super(PrivateMessage, self).__init__(message, sender)
        self.address = address


class MessageToView(Message):
    """Class that creates an object that indicates that a client/admin wants to see the managers list."""
    def __init__(self, sender):
        super(MessageToView, self).__init__(MANAGERS_VIEW_MSG, sender)


class Error(object):
    """Class that indicates that an error had occurred."""
    def __init__(self, error):
        self.error = error




