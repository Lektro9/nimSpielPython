import socket
from PyQt5.QtCore import QThread

HEADERSIZE = 10


class ServerThread(QThread):

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
            try:
                print('connection from', client_address)

                welcome_msg = "You are connected!"
                welcome_msg = f'{len(welcome_msg):<{HEADERSIZE}}' + welcome_msg
                connection.send(bytes(welcome_msg, 'utf-8'))

                # Receive the data in small chunks and retransmit it
                full_msg = ''
                new_msg = True

                while True:
                    msg = connection.recv(16)
                    if new_msg:
                        msglen = int(msg[:HEADERSIZE])
                        new_msg = False

                    full_msg += msg.decode('utf-8')

                    # if the length of the full message minus HEADERSIZE is the same length as the real msglen
                    if len(full_msg)-HEADERSIZE == msglen:
                        print(f'Server: {full_msg}')
                        connection.sendall(bytes(full_msg, 'utf-8'))
                        new_msg = True
                        full_msg = ''

            finally:
                # Clean up the connection
                connection.close()
