import socket
import ssl
import skimage
import numpy
import cv2

if __name__ == '__main__':

    host_ip = '127.0.0.1'
    port = 1234

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(True)
    sock.connect((host_ip, port))

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('server.crt')
    context.load_cert_chain(certfile="client.crt", keyfile="client.key")

    if ssl.HAS_SNI:
        secure_sock = context.wrap_socket(sock, server_side=False, server_hostname=host_ip)
    else:
        secure_sock = context.wrap_socket(sock, server_side=False)

    if not secure_sock.getpeercert(): raise Exception("No server's certificate!")
    print("Sending image")
    image = cv2.imread('Lenna.png', 1)
    noised_image = skimage.util.random_noise(image, mode='s&p', seed=None, clip=True)
    noised_image = numpy.array(255*noised_image, dtype='uint8')
    cv2.imwrite("Lenna_noised.png", noised_image)
    with open("Lenna_noised.png", 'rb') as f:
        bytes_pack = f.read(1024)
        number = 0
        while bytes_pack:
            print("Sending #{0} package of 1024 bytes".format(number))
            secure_sock.send(bytes_pack)
            bytes_pack = f.read(1024)
            number += 1
        print("Sending successful!")
    secure_sock.close()
    sock.close()
