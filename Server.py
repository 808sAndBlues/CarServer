import socket
import threading
import select
import os

from SignalHandler import SignalHandler
from TelemetryProcessor import TelemetryProcessor

class Server(threading.Thread):
    def __init__(self, port: int, address: str, sig_handler: SignalHandler):
        threading.Thread.__init__(self, target= self.main_loop)

        self._port: int = port
        self._addr: str = address
        self._sock: socket.socket = None
        self._epoll: select.epoll = select.epoll()
        self._tlm_processor: TelemetryProcessor = TelemetryProcessor()

        self._sig_handler: SignalHandler = sig_handler

        self.init_sock(self._port, self._addr)
        self.init_epoll()


    def init_epoll(self):
        self._epoll.register(self._sig_handler.get_fileno(), select.EPOLLIN)
        self._epoll.register(self._sock.fileno(), select.EPOLLIN)


    def init_sock(self, port: int, address: str):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_IP)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self._sock.bind((address, port))

    def process(self, fileno):
        if fileno == self._sock.fileno():
            data, addr = self._sock.recvfrom(1024)
              
            print("Server: Received data from: ", addr)
            print(data)
            print()

            self._tlm_processor.process_data(data)


        elif fileno == self._sig_handler.get_fileno():
            os.eventfd_read(fileno)
            print("Server: Shutdown activated!")


    def evaluate_events(self, events):
        for event in events:
            fileno, _ = event
            self.process(fileno)

    def main_loop(self):
        while not self._sig_handler.get_shutdown():
            events = self._epoll.poll()
            self.evaluate_events(events)

