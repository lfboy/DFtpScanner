#!/usr/bin/python


from ftplib import FTP
import socket
import os
import pymongo
import ConfigParser
import time
import threading
import tools

DEBUG = 2
config_file = os.getcwd() + '/config.ini'
cf = ConfigParser.ConfigParser()
cf.read(config_file)
LOG_FILE = os.path.join(os.getcwd(),cf.get('support','log_path'))
logger = tools.set_logger('FtpScanner.py',LOG_FILE)

class FtpScanner:
	def __init__(self,port=21,timeout=5,thread_num=20):
		self.port = port
		self.timeout = timeout
		self.thread_num = thread_num
		self.current_threads = 0
		self.ip_list = []
		self.result_map = []
		self.lock = threading.Lock()
		
	
	def scan(self,server):
		try:
			ftp = FTP()
			ftp.set_debuglevel(DEBUG)
			ftp.connect(server,port=self.port,timeout=self.timeout)
			info = ftp.getwelcome()
			ftp.quit()
		#	logger.info(info)
			return info
		except socket.error,msg:
			if 'refused' in msg[1]:
				info =  'FTP Close!'
			else:
				info = 'Error:' + msg[1]
			return info

	def set_ip_list(self,ips):
		self.ip_list.clear()
		self.ip_list = ips

	def batch_scan(self):
		self.result_map.clear()
		for i in self.ip_list:
			info = self.scan(i)		
			time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
			self.result_map[i] = {'info':info,'time':time}	
		logger.debug('Result:')
		lgger.debug(self.result_map)
		return self.result_map

	def scan2(self,server):
		time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
		try:
			ftp = FTP()
			ftp.set_debuglevel(DEBUG)
			ftp.connect(server,port=self.port,timeout=self.timeout)
			info = ftp.getwelcome()
			ftp.quit()
		#	logger.info(info)
	#		return (info,time)
		except socket.error,msg:
			if 'refused' in msg[1]:
				info =  'FTP Close!'
			else:
				info = 'Error:' + msg[1]
	#		return (info,time)

		self.lock.acquire()
		self.result_map[server] = {'info':info,'time':time}
		self.lock.release()
		return
		

	def batch_scan2(self):
		self.result_map.clear()
		for index in range(len(self.ip_list)):
			if self.current_threads < self.thread_num:	
				t = thread.Threading(target=self.scan2,name='scan sub thread')
				t.setDaemon(1)
				t.start()
				t.join()
			else:
				sleep(INTERVAL)
				index = index - 1
				continue

		#	time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
		#	self.result_map[i] = {'info':info,'time':time}	
		logger.debug('Result:')
		lgger.debug(self.result_map)
		return self.result_map

if __name__=="__main__":
	scanner = FtpScanner()
	scanner.scan('127.0.0.1')
