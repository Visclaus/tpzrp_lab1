import socket


class Server(object):

    def __init__(self, port):
        self.port = port


if __name__ == '__main__':
    server_socket = socket.socket
    server_socket.bind(('', 9090))
