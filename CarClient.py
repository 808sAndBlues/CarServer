import threading
import linuxfd

from sshkeyboard import listen_keyboard, stop_listening
from SignalHandler import SignalHandler

from enum import StrEnum

key_map = {}

class KeyInput(StrEnum):
    UP = 'up',
    DOWN = 'down',
    LEFT = 'left',
    RIGHT = 'right'

def press(key):
    print(f"'{key}' pressed")

    key_map[key] = True

def release(key):
    print(f"'{key}' released")

    key_map[key] = False

class InputProcessor(threading.Thread):
    def __init__(self, sig_handler):
        threading.Thread.__init__(self, target= self.main_loop)
        self._sig_handler = sig_handler


    def get_current_direction(self):
        key = None

        for key_input in KeyInput:
            if key_map.get(str(key_input), False):
                key = key_input
        
        return key


    def main_loop(self):
        key = None
        while not self._sig_handler.get_shutdown():
            key = self.get_current_direction()

            #TODO: Send this data to car
            if key is not None:
                print(str(key))

            pass

        stop_listening()

if __name__ == "__main__":
    sig_handler = SignalHandler()
    ip = InputProcessor(sig_handler)

    ip.start()
    listen_keyboard(on_press=press, on_release= release)
    
