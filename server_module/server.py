import socket
import ssl


class Server(object):

    def __init__(self, port):
        self.port = port


if __name__ == '__main__':
    sock = ssl.wrap_socket(socket.socket(), 'server.key', 'server.crt', True)
    sock.bind(('localhost', 43433))
    sock.listen(10)
    conn, addr = sock.accept()
    data = conn.recv(1024)
