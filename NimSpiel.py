import sys
import socket
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from components.Server import ServerThread
from components.Client import ClientThread
from components.MessageListener import MessageListener

HEADERSIZE = 10

connectedClients = {}

class testUI(QDialog):

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 10000)
    print('connecting to {} port {}'.format(*server_address))

    def __init__(self):
        super(testUI, self).__init__()
        loadUi("test.ui", self)
        # Buttons
        self.host_btn.clicked.connect(self.host_click)
        self.connect_btn.clicked.connect(self.client_click)
        self.enter_nickname.clicked.connect(self.nickname_click)
        self.send_btn.clicked.connect(self.send_msg_client)

# Buttons

    def host_click(self):
        self.worker = ServerThread()
        self.worker.start()
        #ThreadSignals
        self.worker.need_new_server_listener.connect(
            self.evt_need_new_server_listener)

    def send_msg_client(self):
        # Send data
        msg = self.chat_input.text()
        msg = f'{len(msg):<{HEADERSIZE}}' + msg
        self.sock.send(bytes(msg, 'utf-8'))

    def client_click(self):
        self.worker = ClientThread(
            sock=self.sock, server_address=self.server_address)
        self.worker.start()

    def nickname_click(self):
        print(self.nickname_input.text())

# Messages from threads

    def evt_need_new_server_listener(self, socket, addr):
        self.message_worker = MessageListener(socket, addr)
        self.message_worker.start()
        #ThreadSignals
        self.message_worker.get_message.connect(
            self.evt_get_message)
        print("nothing yet ")

    def evt_get_message(self, msg):
        print("message of the other guy: " + msg)


app = QApplication(sys.argv)
mainwindow = testUI()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(670)
widget.setFixedHeight(558)
widget.show()
app.exec_()
