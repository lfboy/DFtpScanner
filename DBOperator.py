#!/usr/bin/python


from ftplib import FTP
import socket
import os
import pymongo
import ConfigParser
from tools import set_logger
import traceback

config_file = os.getcwd() + '/config.ini'
cf = ConfigParser.ConfigParser()
cf.read(config_file)
DB_ADDR = cf.get('mongodb','addr')
DB_PORT = int(cf.get('mongodb','port'),10)
READWRITE_USER = cf.get('mongodb','readwrite_user')
READWRITE_PASSWD = cf.get('mongodb','readwrite_password')
LOG_FILE = os.path.join(os.getcwd(),cf.get('support','log_path'))
logger = set_logger('DBOperator.py',LOG_FILE)

class DBOperator:
	def __init__(self):
		try:
			self.connection = pymongo.Connection(DB_ADDR,DB_PORT)
			#Database
			self.db = self.connection.ftp
			logger.debug('Connected to ftp')
			self.db.authenticate(READWRITE_USER,READWRITE_PASSWD)
			logger.debug('Database authenticate success!')
		except:
			print 'Database connect error!'
			traceback.print_exc()
			logger.error('Database connect error,exit.')
			exit(0)
	
	def insert_to_allocate_queue(self,ip,client):
		#collection
		allocate_queue = (self.db).allocate_queue
		#record = '{\"ip\":\"' + ip +'\",' + '\"client\":\"' + client + '\"}'
		allocate_queue.insert({"_id":ip,"client":client})

	def remove_from_allocate_queue(self,ip):
		allocate_queue = self.db.allocate_queue
		allocate_queue.remove({"_id:":ip})
	
	def insert_to_scanned_queue(self,ip,info,time,client):
		scanned_queue = self.db.scanned_queue
		scanned_queue.insert({"_id":ip,"info":info,"time":time,"client":client})
	
	def clear_allocate_queue(self):
		allocate_queue = self.db.allocate_queue
			
	
if __name__=="__main__":
	test = DBOperator()
	test.insert_to_allocate_queue('127.0.0.1','client1')
	
