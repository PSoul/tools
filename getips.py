import socket
import threading
import Queue
import sys
import requests
import urlparse
from BeautifulSoup import BeautifulSoup

ip_list = []


def worker(domain):
    try:
        ip = socket.gethostbyname(domain)
    except:
        ip = ''
    ip_list.append(ip)


def run(q):
    while True:
        domain = q.get()
        worker(domain)
        q.task_done()


def main():
    domain = sys.argv[1]
    try:
        fname = sys.argv[2]
    except:
        fname = 'ips.txt'
    header = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWeb'
                        'Kit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25'}
    post = {'domain': '%s' % domain, 'b2': 1, 'b3': 1, 'b4': 1}
    res = requests.post('http://i.links.cn/subdomain/', data=post, headers=header)
    soup = BeautifulSoup(res.text)
    q = Queue.Queue()
    a = soup.findAll("div", {'class': 'domain', })
    for i in a:
        text = i.text
        text1 = text.split('.')[1:]
        # print '.'.join(text1)
        up = urlparse.urlparse('.'.join(text1))
        print up.netloc
        q.put(up.netloc)
    for t in range(20):
        t1 = threading.Thread(target=run, args=(q, ))
        t1.setDaemon(True)
        t1.start()
    q.join()
    new_list = set(ip_list)
    new1_list = []
    for item in new_list:
        a = item.split('.')[0:3]
        new1_list.append('.'.join(a))
    f = open(fname, 'a')
    print 'the ip list is:'
    for ip in set(new1_list):
        f.write(ip + '.0/24')
        print ip + '.0/24'
    f.close()

if __name__ == '__main__':
    main()