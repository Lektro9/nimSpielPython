import socket
from PyQt5.QtCore import QThread, pyqtSignal

HEADERSIZE = 10


class ServerThread(QThread):

    need_new_server_listener = pyqtSignal('PyQt_PyObject', tuple)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 10000)

        print('starting up on {} port {}'.format(*server_address))

        sock.bind(server_address)

        # Listen for incoming connections
        sock.listen(2)
        while True:
            # Wait for a connection
            print('waiting for a connection')
            connection, client_address = sock.accept()
            self.need_new_server_listener.emit(connection, client_address)
