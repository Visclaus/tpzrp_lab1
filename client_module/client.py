import socket
import ssl

if __name__ == '__main__':
    data = "Hello".encode()
    serv = ssl.wrap_socket(socket.socket())
    serv.connect(('server_url', 443))
    serv.send(data)