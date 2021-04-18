from PyQt5.QtCore import QThread

HEADERSIZE = 10


class ClientThread(QThread):

    def __init__(self, sock, server_address, parent=None):
        QThread.__init__(self, parent)
        self.sock = sock
        self.server_address = server_address

    def run(self):
        # Connect the socket to the port where the server is listening
        self.sock.connect(self.server_address)

        full_msg = ''
        new_msg = True

        while True:
            msg = self.sock.recv(16)
            if new_msg:
                msglen = int(msg[:HEADERSIZE])
                new_msg = False

            full_msg += msg.decode('utf-8')

            # if the length of the full message minus HEADERSIZE is the same length as the real msglen
            if len(full_msg)-HEADERSIZE == msglen:
                print('full message received')
                print(full_msg[HEADERSIZE:])
                new_msg = True
                full_msg = ''
