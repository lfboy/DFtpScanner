#!/usr/bin/python


from ftplib import FTP
import socket
import os

DEBUG = 2

class FtpScanner:
	def __init__(self,timeout=5):
		pass
			
	def connect(self,server,port=21):
		try:
			ftp = FTP()
			ftp.set_debuglevel(DEBUG)
			ftp.connect(server,port)
		
			print ftp.getwelcome()
			ftp.quit()
		except socket.error,msg:
			if "refused" in msg[1]:
				print "FTP Close!"
			else:
				print "Other error:%s" % msg[1]

class DBOperator:
	def __init__(self,server_ip,user_name,password,port=):
		self.

if __name__=="__main__":
	scanner = FtpScanner()
	scanner.connect('127.0.0.1')
