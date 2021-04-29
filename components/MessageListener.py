import socket
from PyQt5.QtCore import QThread, pyqtSignal

HEADERSIZE = 10


class MessageListener(QThread):

    get_message = pyqtSignal(str)

    def __init__(self, socket, addr, parent=None):
        super(QThread, self).__init__()
        self.socket = socket
        self.addr = addr

    def run(self):
        print("starting the messageListener")
        try:
            print('connection from', self.addr)

            welcome_msg = "You are connected!"
            welcome_msg = f'{len(welcome_msg):<{HEADERSIZE}}' + welcome_msg
            self.socket.send(bytes(welcome_msg, 'utf-8'))

            # Receive the data in small chunks and retransmit it
            full_msg = ''
            new_msg = True

            while True:
                msg = self.socket.recv(16)
                if new_msg:
                    msglen = int(msg[:HEADERSIZE])
                    new_msg = False

                full_msg += msg.decode('utf-8')

                # if the length of the full message minus HEADERSIZE is the same length as the real msglen
                if len(full_msg)-HEADERSIZE == msglen:
                    print(f'Server: {full_msg}')
                    self.socket.sendall(bytes(full_msg, 'utf-8'))
                    new_msg = True
                    full_msg = ''

        finally:
            # Clean up the connection
            self.socket.close()
