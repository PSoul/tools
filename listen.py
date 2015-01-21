import socket
import sys


def main(ip, port):
    address = (ip, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(address)
    sock.listen(5)
    while True:
        connection, address = sock.accept()
        try:
            connection.settimeout(5)
            buf = connection.recv(1024)
            if buf == '1':
                connection.send('welcome to server!')
            else:
                connection.send('please go out!')
        except socket.timeout:
            print 'time out'
        connection.close()

if __name__ == '__main__':
    ip = sys.argv[1]
    port = sys.argv[2]
    main(ip, int(port))