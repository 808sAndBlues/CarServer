import time

from Server import *

ADDRESS: str = "0.0.0.0"
PORT: int    = 65000

if __name__ == "__main__":
    sig_handler: SignalHandler = SignalHandler()
    server: Server = Server(PORT, ADDRESS, sig_handler)
    server.start()


