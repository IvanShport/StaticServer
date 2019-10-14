import socket
from threading import Thread
from handlers import handleSocket

class Server:

    def __init__(self, config):
        self.config = config

    def run(self):
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', 8081))

        sock.listen(1)

        for i in range(self.config.threadCount):
            thrd = Thread(target=handleSocket, args=(sock, self.config.root))
            thrd.start()

