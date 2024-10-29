import socket

PORT = 65000
ADDRESS = ""

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind((ADDRESS, PORT))

    while 1:
        data, addr = sock.recvfrom(1024)
        print(data)
        print(len(data))

