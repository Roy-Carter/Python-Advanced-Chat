# -*- coding: utf-8 -*-
#client backend
from SocketClass import *

#MAGIC STRINGS
JOIN_MESSAGE = "In order to join the lobby first of please enter your username -->"
CONNECTION_CHECK_MSG = ""

LEAVE_MSG = "quit"
DISCONNECT_MSG = "disconnect"

VALID_USERNAME = "ok"
INVALID_USERNAME = " The username you entered is already taken! "

MUTED_MESSAGE = "ehmm.. for some reason you cannot speak here ;)"


class Client(object):
    """
    This class creates an object from type client , this class
    holds all of the information about a specific client such as his name
    if he is an admin and if he is allowed to talk or not
    """
    def __init__(self):
        """
        Constructor
        """
        self.allowed_to_talk = True
        self.name = raw_input(JOIN_MESSAGE)
        self.is_admin = False

    @staticmethod
    def message_input():
        """
        This function purpose is basically to get an input of a message from a client
        and to return it
        """
        while True:
            input_msg = raw_input("")
            return input_msg

    @staticmethod
    def print_message(message_received):
        """
        @The message parameter is the message that the client got from the server.
        This function purpose is to print that message to the client.
        """
        print message_received


