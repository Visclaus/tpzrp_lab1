import os
import socket
import ssl

import cv2
import numpy
from skimage.restoration import denoise_tv_chambolle

if __name__ == '__main__':

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

    if not secure_sock.getpeercert():
        raise Exception("No client's certificate!")
    raw_size = secure_sock.recv(10)
    img_size = int.from_bytes(raw_size, byteorder='big', signed=True)
    f = open("received.png", 'wb')
    bytes_pack = secure_sock.recv(1024)
    number = 1
    while bytes_pack:
        print("Receiving image!")
        print("Receiving #{0} package of 1024 bytes".format(number))
        f.write(bytes_pack)
        bytes_pack = secure_sock.recv(1024)
        number += 1
    print("Receiving successful!")

    secure_sock.close()
    server_socket.close()
    f.close()
    recv_img_size = os.path.getsize('received.png')
    if img_size == recv_img_size:
        print("Success! Images are equal!")
    img = cv2.imread('received.png')
    dst = denoise_tv_chambolle(img, weight=0.2, multichannel=True)
    dst = numpy.array(255 * dst, dtype='uint8')
    cv2.imwrite("Lenna_filtered.png", dst)
