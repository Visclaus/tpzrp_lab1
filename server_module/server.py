import socket
import ssl

import cv2

if __name__ == '__main__':

    # print(repr(secure_sock.getpeername()))
    # print(secure_sock.cipher())
    # print(cert)

    host_ip = '127.0.0.1'
    port = 1234

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host_ip, port))
    server_socket.listen(10)

    client, fromaddr = server_socket.accept()
    secure_sock = ssl.wrap_socket(client, server_side=True, ca_certs="client.crt", certfile="server.crt",
                                  keyfile="server.key", cert_reqs=ssl.CERT_REQUIRED,
                                  ssl_version=ssl.PROTOCOL_TLSv1_2)

    if not secure_sock.getpeercert(): raise Exception("No client's certificate!")
    f = open("received.png", 'wb')
    while True:
        print("Receiving image!")
        try:
            bytes_pack = secure_sock.recv(1024)
        except Exception:
            raise Exception("Server stopped")
        number = 1
        while bytes_pack:
            print("Receiving #{0} package of 1024 bytes".format(number))
            f.write(bytes_pack)
            bytes_pack = secure_sock.recv(1024)
            number += 1
        print("Receiving successful!")
        secure_sock.close()
        server_socket.close()
        f.close()
        img = cv2.imread('received.png')
        dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
        cv2.imwrite("Lenna_filtered.png", dst)
