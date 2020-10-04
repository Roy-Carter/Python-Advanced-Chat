# -*- coding: utf-8 -*-
#Socket
#This class basically is a separated to functions of attributes of socket so instead of me using every single time
#for example , in the "send" category and write those 2 lines over and over again i've decided to build a function
#which will hold it and by that i'm saving some time for myself and instead of writing it over and over again i'm just
#calling the function of it .

import socket
IP = "127.0.0.1"
PORT = 80
LEN_OF_LENGTH = 5


class Socket(object):
    """
    This class purpose is to create an object of a socket in order to make it easy
    for me to create a connection between  the client and the server
    """

    def __init__(self):
        """
        Constructor
        """
        self.socket = socket.socket()
        self.socket.connect((IP, PORT))

    def close(self):
        """
        Closes the socket of a client.
        """
        self.socket.close()

    def send(self, send_out_message):
        """
        @The parameter message over here is the message that the client
        wants to send to the other clients.
        this function activates his ability to send to others by receiving the message
        and activates the sending ability.
        """
        self.socket.send(str(len(send_out_message)).zfill(LEN_OF_LENGTH))
        self.socket.send(send_out_message)

    def receive(self):
        """
        This function purpose is to receive a message from the server
        (which means receive a message from another client/clients)
        """
        while True:
            msg_len = ""
            while len(msg_len) != LEN_OF_LENGTH:
                msg_len += self.socket.recv(LEN_OF_LENGTH - len(msg_len))
            msg_len = int(msg_len)
            msg = ""
            while len(msg) != msg_len:
                msg += self.socket.recv(msg_len - len(msg))
            return msg
