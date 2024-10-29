import os
import signal
import linuxfd

class SignalHandler:
    def __init__(self):

        self._shutdown: bool = False

        self.init_handlers()

    def init_handlers(self):
        signal.signal(signal.SIGINT, self.sigint_handler)
        signal.signal(signal.SIGTERM, self.sigint_handler)

    def sigint_handler(self, signum: int, frame):
        # TODO: Add logger call
        self._shutdown = True

        print("SignalHandler: Received SIGINT")

    def sigterm_handler(self, signum: int, frame):
        #TODO: Add logger call
        os.write(self._eventfd, 1)
        self._shutdown = True

        print("SignalHandler: Received SIGTERM")

    def get_shutdown(self) -> bool:
        return self._shutdown
    
    def get_fileno(self):
        return self._eventfd
    
    def read(self):
        os.read(self._eventfd, 1)


