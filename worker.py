#!/usr/bin/python
import os
import ConfigParser
import tools
import socket
import json
import threading
import thread
import datetime
import string
from DBOperator import DBOperator

config_file = os.getcwd() + '/config.ini'
cf = ConfigParser.ConfigParser()
cf.read(config_file)
SERVER_ADDR = cf.get('client','server_addr')
SERVER_PORT = int(cf.get('client','server_port'),10)
LOG_FILE = os.path.join(os.getcwd(),cf.get('support','client_log'))
logger = tools.set_logger('worker.py',LOG_FILE)

def worker():
	global ip_list[]
	global local_ip
	local_ip = socket.gethostbyname(socket.gethostname())
	s = socket.socket()
	s.connect(SERVER_ADDR,SERVER_PORT)
	s.setblocking(0)
	global conn
	conn = s
	regis = {'cmd':'add_client','client':local_ip}
	try:
		my_send(regis)
		a = conn.recv(10)
		length = string.atoi(a)
		res = b''
		while len(res) < length:
			res = res + conn.recv(4096)
		data = json.loads(res)
	except Exception,e:
		logger.error('Register to server error.')
		exit()
	res = parse(data)
	if res == 'success':
	#register successfully
		
	else:
		logger.error('Server reply a error.')
		exit()

def get_my_ips():
	ip_list=[]
	db = DBOperator()	

def my_send(data):
	i = 0
	length = len(data)*1.0
	while True:
		try:
			res = conn.send(data[i:0])
			if 0 == res:
				logger.debug('Send all')
				return 'success'
			else:
				logger.debug('Send:%d%%' % (i/length*100))
				i += res
		except socket.error,e:
			if e.args[0] == errno.EAGAIN:
				pass
			else:
				logger.error(e)
				break
	return 'error'

def cusrecv(num):
	for i in range(4):
		try:
			res = conn.recv(num)
			if not res:
				logger.info('Connection closed!')
				conn.close()
				break;
			else:
				return res
		except socket.error,e:
			if e.args[0] == errno.EWOULDBLOCK:
				logger.info('EWOULDBLOCK: [%d]' % (i))
				time.sleep(2)
			else:
				logger.error(e)
				break
	return 'error'

def my_recv():
	a = cusrecv(10)
	if a == 'error':
		return 'error'
	length2 = string.atoi(a)
	logger.info('DataLength:%d' % (length2))
	res = b''
	while len(res) < length2:
		try:
			a = cusrecv(4096)
			res = res + a
		except:
			logger.error('Receive data error!')
			exit()
	return res 

def pack_data(data):
	a = ['0']*10
	data = json.dumps(data)
	length3 = len(data)
	length3 = str(length3)
	for i in range(len(length3)):
		a[10-i-1] = length3[len(length3)-i-1]
	res = "".join(a)
	res = res + data
	return res

def parse(data):
	cmd = data['cmd']
	if cmd == 'add_client':
		return data['result']
	elif cmd == 'del_client':
		return data['result']
	elif cmd == 'server_close':
		return data['time']
	return -1
		
