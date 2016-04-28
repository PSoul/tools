#coding=utf-8

import Queue
import threading
import sys
import urllib2
import re

opener = urllib2.build_opener()
opener.addheaders = [("User-Agent", 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWeb''Kit/6'
                                    '00.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25')]
opener.addheaders.append(('Cookie', 'ADMINCONSOLESESSION=pbYvWXBH6FpJ0ldJxPKsQG2Kv8GpKv2kFMpvZSFh1p2h4MT6yk5x!-1963107097'))
q = Queue.Queue()
ports = {'7001', '7002', '7003', '8001', '8002', '9001', '9002', '7021', '7000'}
usernames = {'weblogic', 'system', 'portaladmin', 'guest'}
passwords = {'weblogic', 'weblogic123', 'system', 'portaladmin', 'guest', 'weblogic123456'}


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


def worker(ip, port, username, passwd):
    timeout = 3
    data = {'j_username': username, 'j_password': passwd}
    try:
        url = 'http://' + ip + ':' + port + '/j_security_check'
        urlopen = opener.open(url, timeout=timeout)
    except urllib2.HTTPError, e:
        if e.code == 400:
            url = 'https://' + ip + ':' + port + '/j_security_check'
            urlopen = opener.open(url, timeout=timeout)
    if 'console.portal' in urlopen.read():
        sys.wirte(url + ' success')
    pass


def runner():
    pass


def main():
    pass