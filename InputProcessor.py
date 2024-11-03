import threading

from sshkeyboard import listen_keyboard, stop_listening
from enum import StrEnum

class ArrowKeys(StrEnum):
    UP = 'up',
    DOWN = 'down',
    LEFT = 'left',
    RIGHT = 'right'

async def on_press(key):
    print(key)

    print("*****************************")

def on_release(key):
    print(key)

class InputProcessor(threading.Thread):
    def __init__(self, sig_handler):
        threading.Thread.__init__(self, target= self.process_keys)
        self._sig_handler = sig_handler

    def process_keys(self):
        while not self._sig_handler.get_shutdown():
            listen_keyboard(
                on_press=on_press)
            pass

    def join(self):

        stop_listening()

