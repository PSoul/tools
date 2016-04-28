__author__ = 'PSoul'
from Queue import Queue

q = Queue()

q.put(('abc', 'ca', ''))

a, b ,c = q.get()
if c:
    print 123