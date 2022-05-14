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

    def checkUnexpectedSpace(self):
        if coordinates.count(' ') > 1:
            self.sock.sendall(Messages.SERVER_SYNTAX_ERROR.encode())
            raise RuntimeError()

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
        if()
        self.username = self.username[:-2]
        ascii_value = 0
        for i in self.username:
            ascii_value = ascii_value + ord(i)

        hash = (ascii_value * 1000) % 65536
        print(hash)
        serverhash = hash + serverAuthKeys[int(self.clientkey)] % 65536
        print(serverhash)
        self.sock.sendall((str(serverhash) + "\a\b").encode())
        clienthashGetter = self.recvMessage()
        self.checkkey = next(clienthashGetter)
        if len(self.checkkey[:-2]) == 6:
            self.sock.sendall(Messages.SERVER_SYNTAX_ERROR.encode())
            raise RuntimeError()

        for i in self.checkkey:
            if i == ' ':
                self.sock.sendall(Messages.SERVER_SYNTAX_ERROR.encode())
                raise RuntimeError()

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
            if '.' in item:
                self.sock.sendall(Messages.SERVER_SYNTAX_ERROR.encode())
                raise RuntimeError()
            coordinates.append(int(item))

        print("Coordinates are: {}".format(coordinates))
        return coordinates

    def updatecord(self, loc):
        self.icord = self.fcord
        self.fcord = self.getCoordinates(loc)

    def checkObstacle(self):
        if self.icord == self.fcord:
            self.sock.sendall(Messages.SERVER_TURN_LEFT.encode())
            self.dir = (self.dir + 1) % 4
            next(self.recvMessage())
            self.sock.sendall(Messages.SERVER_MOVE.encode())
            CoordinateGetter = self.recvMessage()
            loc = next(CoordinateGetter)
            self.getCoordinates(loc)
            self.updatecord(loc)

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
        self.checkObstacle()

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
        self.checkObstacle()

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
        self.checkObstacle()

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
        self.checkObstacle()

    def direction(self):
        diff = []
        x = int(self.fcord[0]) - int(self.icord[0])
        diff.append(x)
        y = int(self.fcord[1]) - int(self.icord[1])
        diff.append(y)

        if (diff == [1, 0]):
            print("Direction is East")
            self.dir = Messages.EAST
        elif (diff == [-1, 0]):
            print("Direction is West")
            self.dir = Messages.WEST
        elif (diff == [0, 1]):
            print("Direction is South")
            self.dir = Messages.NORTH
        elif (diff == [0, -1]):
            print("Direction is North!")
            self.dir = Messages.SOUTH
        else:
            self.sock.sendall(Messages.SERVER_TURN_LEFT.encode())
            next(self.recvMessage())
            self.initialMovement()

    def initialMovement(self):
        for i in range(2):
            self.sock.sendall(Messages.SERVER_MOVE.encode())
            locationGetter = self.recvMessage()
            self.loc = next(locationGetter)
            self.icord = self.fcord
            self.fcord = self.getCoordinates(self.loc)
        self.direction()

    def movement(self):

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
