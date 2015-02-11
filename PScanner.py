# -*- coding:utf-8 -*-
# coding = utf-8
# author = PSoul
# version = 3.0
# filename = PScanner.py

import Queue
import threading
import socket
import argparse
import httplib
import sys
import os

port_queue = Queue.Queue()
socket.setdefaulttimeout(3)


def ip2bin(ip):
    b = ""
    inQuads = ip.split(".")
    outQuads = 4
    for q in inQuads:
        if q != "":
            b += dec2bin(int(q), 8)
            outQuads -= 1
    while outQuads > 0:
        b += "00000000"
        outQuads -= 1
    return b


def dec2bin(n, d=None):
    s = ""
    while n > 0:
        if n & 1:
            s = "1"+s
        else:
            s = "0"+s
        n >>= 1
    if d is not None:
        while len(s) < d:
            s = "0"+s
    if s == "": s = "0"
    return s


def bin2ip(b):
    ip = ""
    for i in range(0, len(b), 8):
        ip += str(int(b[i:i+8], 2))+"."
    return ip[:-1]


def listCIDR(c):
    cidrlist=[]
    parts = c.split("/")
    baseIP = ip2bin(parts[0])
    subnet = int(parts[1])
    if subnet == 32:
        print bin2ip(baseIP)
    else:
        ipPrefix = baseIP[:-(32-subnet)]
        for i in range(2**(32-subnet)):
            cidrlist.append(bin2ip(ipPrefix+dec2bin(i, (32-subnet))))
        return cidrlist[1:-1]


def port_run(target, port, timeout, filename, burps):
    header = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWeb'
                        'Kit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25'}
    with open(filename, 'a') as f:
        with open(burps) as b:
            if port == '443' or port == '8443':
                h = httplib.HTTPSConnection(target, port=int(port), timeout=timeout)
            else:
                h = httplib.HTTPConnection(target, port=int(port), timeout=timeout)
            url = target + ':' + port
            try:
                # sys.stdout.write(url + '\r')
                # sys.stdout.flush()
                h.request('HEAD', '/', '', header)
                h_resp = h.getresponse()
                server_str = h_resp.getheader('server')
                sys.stderr.write(url + ' server:' + server_str + '\n')
                f.write(url + ' server: ' + server_str + '\n')
                f.flush()
                print 'try to find 404 page ...'
                h.request('GET', '/sbsbsbcaocaocaonininimma', '', header)
                len_judge = len(h_resp.read())
                for path in b:
                    uri = url + path.strip()
                    sys.stderr.write(uri + ' beginning \r')
                    sys.stderr.flush()
                    try:
                        h.request('GET', path, '', header)
                        resp = h.getresponse()
                        if resp.status == 200:
                            if len(resp.read()) != len_judge:
                                print(uri + 'success')
                                f.write(uri + ' 200' + '\n')
                                f.flush()
                        elif resp.status in (403, 301, 302):
                            print(uri + ' ' + str(resp.status))
                            sys.stderr.write(uri + ' ' + str(resp.status) + '213')
                            sys.stderr.flush()
                            f.write(uri + ' ' + str(resp.status) + '\n')
                            f.flush()
                    except socket.timeout, to:
                        print uri + str(to)
                        continue
                    except Exception, exx:
                        print exx
                        continue
            except socket.timeout, e:
                #print url + str(e)
                pass
            except Exception, ex:
                # print url, ex
                pass


def port_worker(timeout, filename, burps):
    while True:
        port, ip = port_queue.get()
        port_run(ip, port, timeout, filename, burps)
        port_queue.task_done()


if __name__ == '__main__':
    try:
        os.remove('ex')
    except:
        pass
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='ip', help='ip target')
    parser.add_argument('-c', '--threads', dest='threadsnum', help='threads num', type=int, default=125)
    parser.add_argument('-t', '--timeout', dest='timeout', type=int, default=4)
    parser.add_argument('-o', dest='filename', default='result.txt')
    parser.add_argument('-p', dest='ports', help='ports filelist', default='ports.txt')
    parser.add_argument('-b', dest='burps', help='burps filelist', default='burp.txt')
    args = parser.parse_args()
    p = open(args.ports, 'r')
    ports = p.readlines()
    if args.ip:
        if '/' in args.ip:
            ips = listCIDR(args.ip)
            for ip in ips:
                for port in ports:
                    port_queue.put((port.strip(), (str(ip))))
        else:
            ip = args.ip
            for port in ports:
                port_queue.put((port.strip(), (str(ip))))
        for item in range(args.threadsnum):
            t = threading.Thread(target=port_worker, args=(args.timeout, args.filename, args.burps, ))
            t.setDaemon(True)
            t.start()
    else:
        print 'PScanner help'
    port_queue.join()
    p.close()
    print 'exit'
    f = open('ex', 'w')
    f.write('sb')
    f.close()