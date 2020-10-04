# -*- coding: utf-8 -*-
from server import *


def help_newcomers():
    """
    This function purpose is to give an explanations for all the commands that a client
    and an admin could do on the chat
    """
    print "============================================="
    print "Welcome to Roy's Lobby chat!"
    print "============================================="
    print "Before you get right into the talky talk i'll mention out some of the " \
        "commands a client could do and that an admin could do for your convenience"
    print "============================================="
    print "Client:"
    print "============================================="
    print "1) To send out / receive messages from others or to see others talking"
    print "2) You can send a private message to a friend of yours by typing !<username> <message>" \
          "for example: \"!Roy you have a great server over here :D\""
    print "3)As a client you also have the ability to view all the admins names by typing out \"view-managers\""
    print "4)Your last option as a client is to use the command \"quit\" " \
        "in order to leave my server (it'll be sad here without you ;( )"
    print "============================================="
    print "Admin:"
    print "============================================="
    print "1)An admin could kick-out a client by typing out \"getout <username>\""
    print "2)An admin could promote someone to be an admin by typing out \"inviteMan <username>\""
    print "3)An admin could also mute someone in chat by typing out  \"shsh <username> \""
    print "4)An admin can send out a private message  by typing !<username> <message> (same as a client)"
    print "5)Like a client the last option of an admin is to  use the command \"quit\" " \
        "in order to leave my server (it'll be sad here without you ;( )"
    print "============================================="
    print"Thank you , for dedicating your time to read this , when you're ready start up a client as well :D"
    print "============================================="

#Main Server
def main():
    help_newcomers()
    server = Server()
    server.manage_all_clients()
    server.close()


if __name__ == '__main__':
    main()