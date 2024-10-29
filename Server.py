import socket
import threading
import select


from SignalHandler import SignalHandler

class Server(threading.Thread):
    def __init__(self, port: int, address: str, sig_handler: SignalHandler):
        threading.Thread.__init__(self, target= self.main_loop)

        self._port: int = port
        self._addr: str = address
        self._sock: socket.socket = None
        self._poll: select.poll = select.poll()

        self._sig_handler: SignalHandler = sig_handler

        self.init_sock(self._port, self._addr)

    def init_sock(self, port: int, address: str):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_IP)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self._sock.bind((address, port))

    def main_loop(self):
        print("1")


