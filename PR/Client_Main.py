# -*- coding: utf-8 -*-
from Messages import *
from client import *
from threading import Thread
import pickle
#MAGIC STRINGS
SPACE = " "
ADMIN_CHAR = '@'
ADD_ADMIN_MSG = "inviteMan"
MUTE_CLIENT_MSG = "shsh"
KICK_USERS_MSG = "getout"
LEAVE_MSG = "quit"
MESSAGE_MANAGER_VIEW = "view-managers"
VALID_USERNAME = "ok"


def send_message_out(client, my_socket):
    """
    @The parameters are the client object and his socket.
    This function purpose is to send out the message from a client
    to other clients , as long as the client did not ask to leave
    the chat lobby.
    """
    try:
        message_out = ""
        while message_out != LEAVE_MSG or my_socket.receive() != LEAVE_MSG:
            my_socket.send(pickle.dumps(MessageToCheckConnection(client.name)))
            message_out = client.message_input()
            message_type = find_type(client, message_out)
            my_socket.send(pickle.dumps(message_type))
            my_socket.send(pickle.dumps(MessageToCheckConnection(client.name)))
        return
    except:
        return


def get_message_in(client, my_socket):
    """
    @The parameters are the client object and his socket.
    this function purpose is to receive a message from other clients as long as they didn't ask
    to leave .
    """
    try:
        message_in = ""
        while message_in != DISCONNECT_MSG:
            client.print_message(message_in)
            message_in = pickle.loads(my_socket.receive()).message
        return
    except:
        return


def find_type(client, message):

    if message == LEAVE_MSG:
        return MessageToExit(client.name)

    elif KICK_USERS_MSG in message:
            return MessageToKickOut(client.name, message[7:])

    elif ADD_ADMIN_MSG in message:
            return MessageToInviteMan(client.name, message[10:])

    elif MUTE_CLIENT_MSG in message:
            return MessageToQuiet(client.name, message[5:])

    elif PRIVATE_MSG_CHAR == message[0]:
            message = message.split(" ")
            the_message = ""
            for i in range(1, len(message)):
                the_message += message[i] + SPACE
            return PrivateMessage(client.name, the_message, message[0][1:])

    elif MANAGERS_VIEW_MSG == message:
        return MessageToView(client.name)

    else:
        return Message(message, client.name)


def run_program(server_ans, client_socket, client_object):
    while server_ans != VALID_USERNAME:
        print server_ans
        client_object = Client()
        client_socket.send(pickle.dumps(client_object))
        server_ans = pickle.loads(client_socket.receive()).message
    send_out_thread = Thread(target=send_message_out, args=[client_object, client_socket])
    receive_in_thread = Thread(target=get_message_in, args=[client_object, client_socket])
    send_out_thread.start()
    receive_in_thread.start()
    send_out_thread.join()
    receive_in_thread.join()
    client_socket.close()


def main():
    #Client Main
    client_socket = Socket()
    client_object = Client()
    client_socket.send(pickle.dumps(client_object))
    server_ans = pickle.loads(client_socket.receive()).message
    print server_ans
    run_program(server_ans, client_socket, client_object)


if __name__ == '__main__':
    main()