#!/usr/bin/python


from ftplib import FTP
import socket
import os
import pymongo
import ConfigParser
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
		self.ip_list = []
	
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


if __name__=="__main__":
	scanner = FtpScanner()
	scanner.scan('127.0.0.1')
