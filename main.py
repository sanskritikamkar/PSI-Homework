import os
import socket
from time import sleep
from socketwrapper import *

l = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket creation: ip/tcp
l.bind(('localhost', 6667))  # binding the socket to this device, port number 6666
l.listen(10)  # number of clients

while True:

    try:
        c, address = l.accept()  # accept returns newly created socket and address of the client

        newConnection = SocketConnection(c)
        newConnection.checkUsername()
        newConnection.movement()

        c.close()
    except Exception as e:
        c.close()
        print(f" Encounterd an Error {e}")

