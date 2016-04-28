import socket
import threading
import Queue
import requests
import json
import sys
import urlparse
from BeautifulSoup import BeautifulSoup

ip_list = {}
socket.setdefaulttimeout(3)


def worker(domain):
    try:
        ip = socket.gethostbyname(domain)
        a = ip.split('.')[0:3]
        b = '.'.join(a)
    except:
        ip = ''
        b = 'N/A'
    try:
        ip_list[b].append(domain + ':' + str(ip))
    except:
        ip_list[b] = []
        ip_list[b].append(domain + ':' + str(ip))


def run(q):
    while True:
        domain = q.get()
        worker(domain)
        q.task_done()


def main(d_name):
    domain = d_name
    domain_dict = {}
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
        up = urlparse.urlparse('.'.join(text1))
        # print up.netloc
        q.put(up.netloc)
    for t in range(20):
        t1 = threading.Thread(target=run, args=(q, ))
        t1.setDaemon(True)
        t1.start()
    q.join()
    for (k, v) in ip_list.items():
        for va in v:
            domain = va.split(':')[0]
            ip = va.split(':')[1]
            domain_dict[domain] = ip
    print json.dumps(domain_dict)

if __name__ == "__main__":
    domain = sys.argv[1]
    main(domain)
