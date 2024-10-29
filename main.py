from Server import *
import time
ADDRESS: str = "10.0.0.5"
PORT: int    = 65000

if __name__ == "__main__":
    sig_handler: SignalHandler = SignalHandler()
    server: Server = Server(PORT, ADDRESS, sig_handler)


