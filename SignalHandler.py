import os
import signal
import linuxfd
import threading

class SignalHandler:

    def __init__(self):
        self._shutdown: bool = False
        self._eventfd = os.eventfd(0)
        self._lock = threading.Lock()

        self.init_handlers()

    def init_handlers(self):
        signal.signal(signal.SIGINT, self.sigint_handler)
        signal.signal(signal.SIGTERM, self.sigint_handler)

    def shutdown_sequence(self):
        self._lock.acquire()

        os.eventfd_write(self._eventfd, 1)
        self._shutdown = True

        self._lock.release()


    def sigint_handler(self, signum: int, frame):
        # TODO: Add logger call
        self.shutdown_sequence()

        print("SignalHandler: Received SIGINT")

    def sigterm_handler(self, signum: int, frame):
        #TODO: Add logger call
        self.shutdown_sequence()

        print("SignalHandler: Received SIGTERM")


    def get_shutdown(self) -> bool:
        return self._shutdown

    
    def get_fileno(self):
        return self._eventfd

