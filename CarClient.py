import threading
import socket
import select
import linuxfd
import time

from sshkeyboard import listen_keyboard, stop_listening
from SignalHandler import SignalHandler
from enum import StrEnum

HOST = "10.0.0.8"
PORT = 65003

key_map = {}

class KeyInput(StrEnum):
    UP = 'up',
    DOWN = 'down',
    LEFT = 'left',
    RIGHT = 'right'

def press(key):
    key_map[key] = True

def release(key):
    key_map[key] = False

class InputProcessor(threading.Thread):
    def __init__(self, sig_handler):
        threading.Thread.__init__(self, target= self.main_loop)
        self._sig_handler = sig_handler

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                   0)

        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    def get_current_direction(self):
        key = None

        for key_input in KeyInput:
            if key_map.get(str(key_input), False):
                key = key_input
        
        return key
    
    
    def send_data(self, key):
        data = 99

        if key == "up":
            data = 0

        elif key == "right":
            data = 1

        elif key == "down":
            data = 2

        else:
            data = 3

        self._sock.sendto(data.to_bytes(1, "big"), (HOST, PORT))
        print("Sent value of: ", data, "(", key, ")")


    def main_loop(self):
        key = None

        while not self._sig_handler.get_shutdown():
            key = self.get_current_direction()

            #TODO: Send this data to car
            if key is not None:
                self.send_data(key)
            
            time.sleep(0.1)

        stop_listening()

if __name__ == "__main__":
    sig_handler = SignalHandler()
    ip = InputProcessor(sig_handler)

    ip.start()
    listen_keyboard(on_press=press, on_release= release)
    
