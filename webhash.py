#!/usr/bin/env python
#coding=utf-8
#create by kiss 

import hashlib
import os
import urllib
import time
import sys

"""计算文件的HASH值"""
def sha1_file(filePath):
	if not os.path.exists(filePath):
		return None
	md5 = hashlib.sha1()
	with open(filePath, 'rb') as _file:
		md5.update(_file.read())
		_file.close()
		return md5.hexdigest()


"""下载文件并按照时间保存"""
def down_file(url):
	strTime = str(time.time())
	save_file = strTime[:strTime.index(".")]
	urllib.urlretrieve(url, save_file)
	if not os.path.exists(save_file):
		return None
	return save_file


class VHash():
	"""docstring for VHash"""
	def __init__(self):
		pass
		
	"""扫描hash文件"""
	def scan_hash_file(self):
		path = os.getcwd() + "/hash/"
		self.fileList  =[]
		for _file in os.listdir(path):
			self.fileList.append(path + "/" + _file)

	"""载入hash数据"""
	def load_hash_data(self):
		self.hashList = []
		for _file in self.fileList:
			fp = open(_file,"rb")
			for string in fp.readlines():
				self.hashList.append(eval(string))
			fp.close()
		self.hashList

	"""解析hash数据"""
	def parse_hash(self):
		self.dircHash = {}
		for key, hashValue, CMSName in self.hashList:
			if self.dircHash.has_key(key):
				self.dircHash[key][hashValue] = CMSName
			else:
				self.dircHash[key] = {hashValue: CMSName}

	def get_hash_path(self):
		return self.dircHash.keys()


	def search_hash(self,key,hashValue):
		if key is None or hashValue is None:
			return None
		if self.dircHash.has_key(key) and self.dircHash[key].has_key(hashValue):
			return self.dircHash[key][hashValue]
		return None


if __name__ == '__main__':
	url = sys.argv[1]
	_vhash = VHash()
	_vhash.scan_hash_file()
	_vhash.load_hash_data()
	_vhash.parse_hash()
	listPath = _vhash.get_hash_path()
	for path in listPath:
		load_file = down_file(url + path)
		md5_data = sha1_file(load_file)
		os.unlink(load_file)
		CMSName = _vhash.search_hash(path, md5_data)
		if CMSName is not None:
			sys.stdout.write(url + path + "----->" + md5_data + "---->" + CMSName + "\n")
		time.sleep(0.01)