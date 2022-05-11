# This project is made by Sanskriti Kamkar for BIE-PSI
import select

import Messages

serverAuthKeys = [23019, 32037, 18789, 16443, 18189]
clientAuthKeys = [32037, 29295, 13603, 29533, 21952]


class SocketConnection:

    def __init__(self, connection):
        self.sock = connection
        self.icord = None
        self.fcord = None
        self.dir = None
        self.message = self.sock.recv(1024).decode()
        self.username = None
        self.clientkey = None
        self.checkkey = None
        self.west = None
        self.east = None
        self.north = None
        self.south = None
        self.loc = None
        self.sock.settimeout(1)

    def recvMessage(self):
        # check if you have some message until end seq in self.message
        if "\a\b" in self.message:
            find_seq = self.message.find("\a\b")
            full_message = self.message[:find_seq + 2]
            self.message = self.message[find_seq + 2:]
            yield full_message
        # if yes then return
        else:
            while True:
                temp = self.sock.recv(1024).decode()
                self.message += temp
                while self.message.count("\a\b") > 0:
                    find_seq = self.message.find("\a\b")
                    full_message = self.message[:find_seq + 2]
                    self.message = self.message[find_seq + 2:]
                    yield full_message

    def checkUsername(self):
        nextMessageGetter = self.recvMessage()
        self.username = next(nextMessageGetter)
        print(self.username)
        print(len(self.username))

        if len(self.username) > 20:
            self.sock.sendall(Messages.SERVER_SYNTAX_ERROR.encode())
            raise RuntimeError()

        self.sock.sendall(Messages.SERVER_KEY_REQUEST.encode())
        clientkeyGetter = self.recvMessage()
        self.clientkey = next(clientkeyGetter)
        self.clientkey = self.clientkey[:-2]

        if self.clientkey.isdigit():
            pass
        else:
            self.sock.sendall(Messages.SERVER_SYNTAX_ERROR.encode())
            raise RuntimeError()

        self.clientkey = int(self.clientkey)

        if (self.clientkey < 0) or (self.clientkey > 4):
            self.sock.sendall(Messages.SERVER_KEY_OUT_OF_RANGE_ERROR.encode())
            raise RuntimeError()

        self.username = self.username[:-2]
        a = 0
        for i in self.username:
            a = a + ord(i)

        hash = (a * 1000) % 65536
        print(hash)
        serverhash = hash + serverAuthKeys[int(self.clientkey)] % 65536
        print(serverhash)
        self.sock.sendall((str(serverhash) + "\a\b").encode())
        clienthashGetter = self.recvMessage()
        self.checkkey = next(clienthashGetter)
        clienthash = (hash + clientAuthKeys[int(self.clientkey)]) % 65536
        print(clienthash)
        if ((str(clienthash) + "\a\b")) == self.checkkey:
            self.sock.sendall(Messages.SERVER_OK.encode())
        else:
            self.sock.sendall(Messages.SERVER_LOGIN_FAILED.encode())
            raise RuntimeError()

        print("Authentication Complete!")

    def getCoordinates(self, coordinates):
        coordinates = coordinates[:-2]
        coordinates = coordinates.split()
        actual_coordinates = coordinates[1:]
        coordinates = []
        print("Coordinates are: {}".format(actual_coordinates))
        for item in actual_coordinates:
            coordinates.append(int(item))
        print("Coordinates are: {}".format(coordinates))
        return coordinates

    def updatecord(self,loc):
        self.icord = self.fcord
        self.fcord = self.getCoordinates(loc)
        # if self.icord == self.fcord:
        #     self.sock.sendall(Messages.SERVER_TURN_RIGHT.encode())
        #     next(self.recvMessage())
        #     self.sock.sendall(Messages.SERVER_MOVE.encode())
        #     next(self.recvMessage())

    def moveEast(self):
        if self.dir == Messages.NORTH:
            self.sock.sendall(Messages.SERVER_TURN_RIGHT.encode())
            next(self.recvMessage())

        elif self.dir == Messages.WEST:
            self.sock.sendall(Messages.SERVER_TURN_RIGHT.encode())
            next(self.recvMessage())
            self.sock.sendall(Messages.SERVER_TURN_RIGHT.encode())
            next(self.recvMessage())

        elif self.dir == Messages.SOUTH:
            self.sock.sendall(Messages.SERVER_TURN_LEFT.encode())
            next(self.recvMessage())

        elif self.dir == Messages.EAST:
            pass

        self.sock.sendall(Messages.SERVER_MOVE.encode())
        eastMover = self.recvMessage()
        self.east = next(eastMover)
        self.dir = Messages.EAST
        self.getCoordinates(self.east)
        self.updatecord(self.east)

    def moveWest(self):
        if self.dir == Messages.NORTH:
            self.sock.sendall(Messages.SERVER_TURN_LEFT.encode())
            next(self.recvMessage())

        elif self.dir == Messages.WEST:
            pass

        elif self.dir == Messages.SOUTH:
            self.sock.sendall(Messages.SERVER_TURN_RIGHT.encode())
            next(self.recvMessage())

        elif self.dir == Messages.EAST:
            self.sock.sendall(Messages.SERVER_TURN_LEFT.encode())
            next(self.recvMessage())
            self.sock.sendall(Messages.SERVER_TURN_LEFT.encode())
            next(self.recvMessage())

        self.sock.sendall(Messages.SERVER_MOVE.encode())
        westMover = self.recvMessage()
        self.west = next(westMover)
        self.dir = Messages.WEST
        self.getCoordinates(self.west)
        self.updatecord(self.west)

    def moveNorth(self):
        if self.dir == Messages.NORTH:
            pass

        elif self.dir == Messages.WEST:
            self.sock.sendall(Messages.SERVER_TURN_RIGHT.encode())
            next(self.recvMessage())

        elif self.dir == Messages.SOUTH:
            self.sock.sendall(Messages.SERVER_TURN_RIGHT.encode())
            next(self.recvMessage())
            self.sock.sendall(Messages.SERVER_TURN_RIGHT.encode())
            next(self.recvMessage())

        elif self.dir == Messages.EAST:
            self.sock.sendall(Messages.SERVER_TURN_LEFT.encode())
            next(self.recvMessage())

        self.sock.sendall(Messages.SERVER_MOVE.encode())
        northMover = self.recvMessage()
        self.north = next(northMover)
        self.dir = Messages.NORTH
        self.getCoordinates(self.north)
        self.updatecord(self.north)

    def moveSouth(self):
        if self.dir == Messages.NORTH:
            self.sock.sendall(Messages.SERVER_TURN_RIGHT.encode())
            next(self.recvMessage())
            self.sock.sendall(Messages.SERVER_TURN_RIGHT.encode())
            next(self.recvMessage())

        elif self.dir == Messages.WEST:
            self.sock.sendall(Messages.SERVER_TURN_LEFT.encode())
            next(self.recvMessage())

        elif self.dir == Messages.SOUTH:
            pass

        elif self.dir == Messages.EAST:
            self.sock.sendall(Messages.SERVER_TURN_RIGHT.encode())
            next(self.recvMessage())

        self.sock.sendall(Messages.SERVER_MOVE.encode())
        southMover = self.recvMessage()
        self.south = next(southMover)
        self.dir = Messages.SOUTH
        self.getCoordinates(self.south)
        self.updatecord(self.south)

    def movement(self):
        for i in range(2):
            self.sock.sendall(Messages.SERVER_MOVE.encode())
            locationGetter = self.recvMessage()
            self.loc = next(locationGetter)
            self.icord = self.fcord
            self.fcord = self.getCoordinates(self.loc)

        diff = []
        a = int(self.fcord[0]) - int(self.icord[0])
        diff.append(a)
        b = int(self.fcord[1]) - int(self.icord[1])
        diff.append(b)

        if (diff == [1, 0]):
            print("Direction is East")
            self.dir = Messages.EAST
        if (diff == [-1, 0]):
            print("Direction is West")
            self.dir = Messages.WEST
        if (diff == [0, 1]):
            print("Direction is South")
            self.dir = Messages.NORTH
        if (diff == [0, -1]):
            print("Direction is North!")
            self.dir = Messages.SOUTH

        while self.fcord != [0, 0]:

            while self.fcord[1] < 0:
                self.moveNorth()

            while self.fcord[1] > 0:
                self.moveSouth()

            while self.fcord[0] < 0:
                self.moveEast()

            while self.fcord[0] > 0:
                self.moveWest()

        self.sock.sendall(Messages.SERVER_PICK_UP.encode())
        next(self.recvMessage())
        self.sock.sendall(Messages.SERVER_LOGOUT.encode())
