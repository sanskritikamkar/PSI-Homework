import socket

#  This function check for end sequence \a\b
#
#
def getMessage(self):

    while True:
        tmp = self.sock.recv(1024).decode()
        self.message += tmp
        while self.message.count("\a\b") > 0:
            endS_ID = self.message.find("\a\b")
            next = self.message[:endS_ID + 2]
            yield next




    #usernmae\a\b2\a\b65434\a\b"

    #OO
    #mpa
    #\a\b

