# -*- coding: utf-8 -*-
from Messages import *
import socket
from client import Client
import DataBaseClass
from select import select
import pickle
import datetime
from SocketClass import *
from DataBaseClass import *
#MAGIC STRINGS
IP = "127.0.0.1"
PORT = 80
CLIENTS_AMOUNT_LISTEN = 10
LEN_OF_LENGTH = 5
AT_SIGN = "@"
SPACE = " "
POINTS_FOR_TIME = ":"
POINTS_WITH_SPACE = ": "
CLIENT_KICK_MSG_P1 = "The client "
CLIENT_KICK_MSG_P2 = " was kicked out of the server because an admin decided to :)"
CLIENT_KICK_BROADCAST_MSG_P2 = " has decided to leave the chat.. we'll miss you!"
ADMINS_LIST_PRINT_OUT_P1 = " managers online --> || "
ADMINS_LIST_PRINT_OUT_P2 = " || "

CONNECTION_CHECK = ""
WELCOME_MSG = " has connected , give him a warm welcome in chat :) "
USER_ALREADY_EXISTS = "This name is already in the chat ! please choose another username."
INVALID_USERNAME = "your username is invalid"
VALID_USERNAME = "ok"
NO_PERM_BECAUSE_NO_ADMIN = "Whoops its an error! why did you try a command you have no permissions for :? ;)"
NOT_A_CLIENT = "Error ! the username you entered is not a client in the server!"

FIRST_ADMIN_JOIN = "admin"
ADMIN_CHAR = '@'
ADD_ADMIN_MSG = "inviteMan"
RANK_UP_MSG = "You have just been promoted to admin , congratulations!"
KICKED_OUT_MSG = "You were kicked by an admin!"
NO_PERM_TO_TALK = "You cannot speak here .. I wonder why ... ;)"
MUTE_MSG = "You were muted by an admin!"
MUTE_CLIENT_MSG = "shsh"
KICK_USERS_MSG = "getout"
LEAVE_MSG = "quit"
DISCONNECT_MSG = "disconnect"
MESSAGE_MANAGER_VIEW = "view-managers"
PRIVATE_MSG_CHAR = "!"


class Server(object):
    """
    This class purpose is to create an object of a server which will help to provide communication between
    clients and allow them to talk / send private messages without an interference
    """
    def __init__(self):
        """
        Constructor
        """
        self.server_socket = socket.socket()
        self.listen()
        self.db = DataBase()

    def find_socket_in_data(self, name_to_bring_socket):
        """
        @The parameter name_to_bring_socket is the name of a client that we want to find his socket.
        This function purpose is to find the client which owns this name and to return his socket.
        """
        for socket_check in self.db.online_clients:
            if self.db.clients_and_sockets[socket_check].name == name_to_bring_socket:
                return socket_check
        raise ClientDoesNotExists

    @staticmethod
    def receive(sender_socket):
        """
        @The  parameter sender_socket holds the socket of the sender of a message.
        This function purpose is to receive a message sent by a client.
        """
        msg_len = ""
        while len(msg_len) != LEN_OF_LENGTH:
            msg_len += sender_socket.recv(LEN_OF_LENGTH - len(msg_len))
        msg_len = int(msg_len)
        msg = ""
        while len(msg) != msg_len:
            msg += sender_socket.recv(msg_len - len(msg))
        return msg

    def listen(self):
        """
        This function allows the server to be able to use the attribute of a socket called
        listen and by that treat a few clients in once.
        this function starts up this process.
        """
        self.server_socket.bind((IP, PORT))
        self.server_socket.listen(CLIENTS_AMOUNT_LISTEN)

    def close(self):
        """
        This function only purpose is to use the attribute of a socket named close and to
        close up the socket .
        """
        self.server_socket.close()

    def get_out_client(self, client_s, to_kick_name):
        """
        @The client_s parameter is the socket of the client which sent the message.
        @name_to_kick parameter is the name of the user the user that needs to be kicked.
        This function purpose is to first off check if the person that asked to kick someone is an admin ,
        if so executes a kick and deletes the person who got kicked from the data-base
        and disconnects him from the server.
        if the guy who asked to preform the action isn't an admin / tried to commit it on a client that does not
        exist or on an admin , an exception will be raised.
        """
        try:
            self.db.check_if_admin(client_s)
            if AT_SIGN+to_kick_name in self.db.admins_names_list:
                to_kick_name = AT_SIGN+to_kick_name
            client_to_kick_socket = self.find_socket_in_data(to_kick_name)
            self.remove_a_client(client_to_kick_socket)
        except NotAnAdmin:
            self.send(NO_PERM_BECAUSE_NO_ADMIN, client_s)
        except ClientDoesNotExists:
            self.send(NOT_A_CLIENT, client_s)

    def save_and_connect_new_client(self):
        """
        This function purpose is to connect a new client to the server and after it connects him to the server
        lobby it adds his socket to the server data-base
        """
        (client_socket, client_address) = self.server_socket.accept()
        self.db.socket_insert(client_socket)
        self.prepare_and_load_client_object(client_socket)

    def msg_everyone(self, message, client_socket):
        """
        @the broadcast_msg parameter is the message that the sender wants to send to all the clients.
        @the sender_socket parameter is the socket owned by the sender.
        This function purpose is to send out a broadcast message to everyone except , the sender himself , which already
        has the message because he is the one who sent it out.
        """
        for client in self.db.online_clients:
            if not (client is client_socket):
                self.send(message, client)

    def task_manager(self, message, client_socket):
        """
        @The message_to_check parameter is a message that the server needs to check so if the client asked
        for a specific command it'll execute it.
        @The sender_socket parameter is the socket which sent out the message to the server.
        This function purpose is to check for a specific request from a client and to execute it :
        for example to quit,view-managers,send private messages etc etc..
        """
        if isinstance(message, MessageToExit):
            self.client_has_disconnected(client_socket)
        elif not self.db.clients_and_sockets[client_socket].allowed_to_talk:
            self.send(NO_PERM_TO_TALK, client_socket)
        elif isinstance(message, MessageToKickOut):
            self.get_out_client(client_socket, message.to_kick)

        elif isinstance(message, MessageToInviteMan):
            self.promote_to_admin(client_socket, message.to_invite)

        elif isinstance(message, MessageToQuiet):
            self.mute_a_user(client_socket, message.to_shsh)

        elif isinstance(message, PrivateMessage):
            self.private_communication_manager(client_socket, message.address, message.message)

        elif isinstance(message, MessageToView):
            self.send(str(self.db.admins_names_list), client_socket)

        else:
            now = datetime.datetime.now()
            text = str(now.hour) + POINTS_FOR_TIME + str(now.minute) + SPACE + \
                      self.db.clients_and_sockets[client_socket].name + POINTS_WITH_SPACE + message.message
            self.msg_everyone(text, client_socket)

    @staticmethod
    def send(send_out_msg, receiver_socket):
        """
        @The parameter send_out_msg is the message that the server needs to send out.
        @The receiver_socket parameter is the socket of the client that the server needs to send the message to.
        Overall , this function sends out a message that it got as a parameter to
        a client which it also got as a parameter.
        """
        send_out_msg_obj = Message(send_out_msg, "server")
        receiver_socket.send(str(len(pickle.dumps(send_out_msg_obj))).zfill(LEN_OF_LENGTH))
        receiver_socket.send(pickle.dumps(send_out_msg_obj))

    def private_communication_manager(self, sender_socket, address_name, message_from_sender):
        """
        @The sender_socket parameter is the socket of the guy who has requested to send a private message.
        @The address_name is the name of the guy which he want to send the message to.
        @The message_from_sender parameter is the message that the sender asked to send to the address.
        This function purpose is to allow a client to send to another client a private
        as long as the client he wants to send the message to actually exists.
        """
        try:
            now = datetime.datetime.now()
            if AT_SIGN + address_name in self.db.admins_names_list:
                address_name = AT_SIGN + address_name
            addressee_socket = self.find_socket_in_data(address_name)
            message = str(now.hour) + POINTS_FOR_TIME + str(now.minute) + SPACE + PRIVATE_MSG_CHAR + \
            self.db.clients_and_sockets[sender_socket].name + POINTS_WITH_SPACE + message_from_sender
            print message_from_sender
            self.send(message, addressee_socket)
        except ClientDoesNotExists:
            self.send(NOT_A_CLIENT, sender_socket)

    def get_all_admins(self, client_socket):
        """
        @The parameter client_socket is a socket of a client who asked to view the managers list.
        This function purpose is to send to the client who asked for a list of the managers the list.
        """
        admins = ADMINS_LIST_PRINT_OUT_P1
        for admin in self.db.admins_names_list:
            admins += admin + ADMINS_LIST_PRINT_OUT_P2
        self.send(admins, client_socket)

    def manage_all_clients(self):
        """
        This function purpose is to take care of all the clients which want to join the server / send a message.
        """
        while True:
            rlist, wlist, xlist = select(self.db.online_clients + [self.server_socket], [], [])
            for r_socket in rlist:
                if r_socket is self.server_socket:
                    self.save_and_connect_new_client()
                else:
                    msg = pickle.loads(self.receive(r_socket))
                    if not isinstance(msg, MessageToCheckConnection):
                        self.task_manager(msg, r_socket)

    def promote_to_admin(self, client_sender, name_to_promote):
        """
        @The client_sender parameter is the socket which sent the command with the message.
        @name_to_promote parameter is the name of the guy who needs to rank up to admin.
        This function purpose is to upgrade a client to an admin , but only if the guy that sent the command
        to upgrade him is an admin too , if not raises an exception , if he is an admin and he tries to promote someone
        who does not exists it will also raise an exception.
        """
        try:
            self.db.check_if_admin(client_sender)
            client_to_admin_socket = self.find_socket_in_data(name_to_promote)
            self.db.insert_admin_to_list(client_to_admin_socket)
            self.send(RANK_UP_MSG, client_to_admin_socket)
        except NotAnAdmin:
            self.send(NO_PERM_BECAUSE_NO_ADMIN, client_sender)
        except ClientDoesNotExists:
            self.send(NOT_A_CLIENT, client_sender)

    def mute_a_user(self, sender_socket, need_to_mute_user):
        """
        @sender_socket parameter is the socket of the sender of the message.
        @user_to_mute parameter is the name of the user to mute
        This function purpose is to check whether a user that sent the shsh command is an admin , if so mute
        the guy that he wrote his name and sent it as a parameter .
        if the client he wants to mute does not exists at all  raise an exception of inexistence.
        if the guy who sent the command is not an admin raise an exception of not an admin
        """
        try:
            self.db.check_if_admin(sender_socket)
            if AT_SIGN + need_to_mute_user in self.db.admins_names_list:
                need_to_mute_user = AT_SIGN + need_to_mute_user
            client_to_shsh_socket = self.find_socket_in_data(need_to_mute_user)
            self.db.clients_and_sockets[client_to_shsh_socket].allowed_to_talk = False
            self.send(MUTE_MSG, client_to_shsh_socket)
        except NotAnAdmin:
            self.send(NO_PERM_BECAUSE_NO_ADMIN, sender_socket)
        except ClientDoesNotExists:
            self.send(NOT_A_CLIENT, sender_socket)

    def remove_a_client(self, disconnect_socket):
        """
        @The disconnect_socket parameter is the socket which needs to get kicked out of the server.
        This function purpose is to receive a socket of a client that an admin kicked and to remove him from
        the chat and also to delete him from the data-base.
        """
        self.send(KICKED_OUT_MSG, disconnect_socket)
        self.send(DISCONNECT_MSG, disconnect_socket)
        disconnect_socket.close()
        self.msg_everyone(CLIENT_KICK_MSG_P1 + self.db.clients_and_sockets[disconnect_socket].name
                        + CLIENT_KICK_MSG_P2, disconnect_socket)
        self.db.remove_disconnected_client(disconnect_socket)

    def prepare_and_load_client_object(self, client_s_pickle):
        """
        @client_s_pickle parameter is the client socket of which I received the pickled client object from.
        This function purpose is to load the object pickle to a string and to add it to the client that sent it to
        the server data-base.
        This function loads the client object and adds him to the data-base as an admin if he is or as a user
        as long as he does not enter a name which is already taken ,
        if he does it sends him a message telling him to re-enter a name , after he'll fix
        the username the server will accept the object and he will be saved in the data-base of the server.
        """
        try:
            str_of_a_client = self.receive(client_s_pickle)
            client_object = pickle.loads(str_of_a_client)
            self.db.new_client_insert(client_s_pickle, client_object)
            self.send(VALID_USERNAME, client_s_pickle)
            self.msg_everyone(client_object.name + WELCOME_MSG, client_s_pickle)
            if client_object.name == FIRST_ADMIN_JOIN:
                self.db.insert_admin_to_list(client_s_pickle)
        except NameAlreadyExists:
            self.send(USER_ALREADY_EXISTS, client_s_pickle)
        except IllegalName:
            self.send(INVALID_USERNAME, client_s_pickle)

    def client_has_disconnected(self, client_s):
        """
        @The client_socket parameter is the socket which want to disconnect from the server.
        This function purpose is to receive a socket who asks to disconnect and to disconnect it from the chat
        and also to remove him from the data-base so he won't take a name that someone else might be wanting to use.
        """
        self.send(DISCONNECT_MSG, client_s)
        self.msg_everyone(CLIENT_KICK_MSG_P1 + self.db.clients_and_sockets[client_s].name
                        + CLIENT_KICK_BROADCAST_MSG_P2, client_s)
        client_s.close()
        self.db.remove_disconnected_client(client_s)


