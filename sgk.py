# -*- encoding: utf-8 -*-

import re
import urllib2
import sys

def curl(username):
	uri = "http://p.08lt.com/p.asp?wd=%s" %username
	rs = urllib2.urlopen(uri)
	res = rs.read()
	re1 = re.findall(r'<td>.*?</td>', res)
	print reduce(lambda s, (idx, x): (s.replace('<td>', '').replace('</td>', '') + str(x) + (',' if (idx+1) % 6 else '\n')), enumerate(re1), '')

if __name__ == '__main__':
	usr = sys.argv[1]
	curl(usr)