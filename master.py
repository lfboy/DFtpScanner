#!/usr/bin/python
import os
from tools import set_logger
import socket
import json
import threading
import datetime
import string

config_file = os.getcwd() + '/config.ini'
cf = ConfigParser.ConfigParser()
cf.read(config_filei)
MIN_CLIENTS = int(cf.get('server','min_clients'),10)
LOG_FILE = os.path.join(os.getcwd(),cf.get('support','log_file'))
logger = set_logger('Master.py',LOG_FILE)

class Client;
	def __init__(self, ip, level = 1, status = True):
		self.ip = ip
		self.level = level
		sefl.status = status
	def set_status(self,status):
		self.status = status
	def get_status(self,status):
		return self.status
	

class Master:
	def __init__(self):
		self.clients = get_clients()
		self.client_num = self.clients.length()
		str_ip_start = raw_input('IP Start:')
		str_ip_end = raw_input('IP End:')
		self.ip_start = ip2long(str_ip_start)
		self.ip_end = ip2long(str_ip_end)			
		pass
	def get_clients(self):
		pass
	def add_client(self,client):
		self.clients.insert(client)
		self.client_num += 1
		pass
	def del_client(self,client):
		for i in self.clients:
			if i.ip = client.ip:
				self.clients.
			
		pass
	def __allocate(self):
		if self.client_num < MIN_CLIENTS:
			return
		for i in self.clients:
						
		pass

class Server:
	TIMEOUT = 60
	PORT = 6600
	s = socket.socket()
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	host = socket.gethostname()
	port = PORT
	s.bind((host,port))
	s.listen(5)
	while True:
		logger.info('Ready to connect!')
		try:
			c,addr = s.accept()
			logger.info('Got guest from ' + addr)
			try:
				t = ClientAdder(c)
				t.start()
			except Exception e:
				logger.error(e)
		except:
			logger.info('Time out.')
			continue

class DataHandler:
	def pack_data(self,data):
		a = ['0']*10
		data = json.dumps(data)
		length = len(data)
		length = str(length)
		for i in range(len(length)):
			a[10-i-1] = length[len(length)-i-1]
		res = ''.join(a)
		res = res + data
		return res
	def parse(self,data):
		cmd = data['cmd']
		if cmd == 'add'
