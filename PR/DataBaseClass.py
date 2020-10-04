# -*- coding: utf-8 -*-
#DataBase
#MAGIC STRINGS
CHAR_THAT_PRESENTS_ADMINS = '@'


class ClientDoesNotExists(Exception):
    pass


class NotAnAdmin(Exception):
    pass


class NameAlreadyExists(Exception):
    pass


class IllegalName(Exception):
    pass


class DataBase(object):
    """
    This class purpose is to store all the database of the server .
    for example : the admins list and names and the clients that are connected.
    this class makes it easy for me to reach out to specific clients or admins name or socket.
    """
    def __init__(self):
        """
        Constructor
        """
        self.clients_and_sockets = {}
        self.online_clients = []
        self.client_names = []
        self.admins_socket_list = []
        self.admins_names_list = []

    def socket_insert(self, client_socket):
        """
        @The parameter client_socket is the socket of a user that the server would like to add to the online
        socket list in order to be able to send him messages.
        """
        self.online_clients.append(client_socket)

    def new_client_insert(self, client_socket, object_of_a_client):
        """
        @The parameter client_socket is the socket that the server received from someone who send the object
        and the @client_object is the object that the server received and needs to add to the dictionary of clients
        and sockets. this function purpose is to add the client socket and object to the dictionary of sockets and clients
        only if the username of the objects in not already taken , if it does the function raises an exception
        """
        if object_of_a_client.name in self.client_names:
            raise NameAlreadyExists
        elif object_of_a_client.name[0] == CHAR_THAT_PRESENTS_ADMINS:
            raise IllegalName
        #self.clients_and_sockets.keys().append(client_socket)
        self.clients_and_sockets[client_socket] = object_of_a_client
        self.client_names.append(object_of_a_client.name)
        return True

    def remove_disconnected_client(self, socket):
        """
        @the client_sockets parameter is the socket that the server needs to disconnect it from .
        this function purpose is to remove and delete the socket and the client object from all of the lists
        and dictionary because the client have decided to disconnect.
        """
        object_client = self.clients_and_sockets[socket]

        if object_client.is_admin:
            self.admins_socket_list.remove(object_client)
            self.admins_names_list.remove(object_client.name)
            self.client_names.remove(object_client.name[1:])
        else:
            self.client_names.remove(object_client.name)
        del[self.clients_and_sockets[socket]]
        self.online_clients.remove(socket)

    def check_if_admin(self, client_socket):
        """
        @the parameter client_socket is the socket of a client that I would like to check his administration
        in order to find out if he is a client or an admin
        """
        if not self.clients_and_sockets[client_socket].is_admin:
            raise NotAnAdmin

    def insert_admin_to_list(self, transfer_to_admin_socket):
        """
        @the parameter is a client socket which needs to become an admin because another admin
        invited him to be.
        this function purpose is to add the client name and socket into the admins lists in order to him to be counted
        as an admin .
        """
        client = self.clients_and_sockets[transfer_to_admin_socket]
        client.is_admin = True
        client.name = CHAR_THAT_PRESENTS_ADMINS + client.name
        self.admins_socket_list.append(client)
        self.admins_names_list.append(client.name)
