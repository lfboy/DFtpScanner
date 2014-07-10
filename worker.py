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
import traceback
import time
from DBOperator import DBOperator
from FtpScanner import FtpScanner

config_file = os.getcwd() + '/config.ini'
cf = ConfigParser.ConfigParser()
cf.read(config_file)
SERVER_ADDR = cf.get('client','server_addr')
SERVER_PORT = int(cf.get('client','server_port'),10)
IP_STEP = int(cf.get('client','step'),10)
TIMEOUT = int(cf.get('client','timeout'),10)
INTERVAL = int(cf.get('client','interval'),10)
LOG_FILE = os.path.join(os.getcwd(),cf.get('support','client_log'))
logger = tools.set_logger('worker.py',LOG_FILE)

def worker():
	global ip_list
	global result_map
	global local_ip

	ip_list = []
	result_map = dict()	
	local_ip = tools.get_local_ip('eth0')
#	print local_ip,SERVER_ADDR,SERVER_PORT

	conn = myconnect(SERVER_ADDR,SERVER_PORT)
	time.sleep(2)
	tmp = {}
	tmp['cmd'] = 'add_client'
	tmp['client'] = local_ip
	regis = pack_data(tmp)
	try:
		my_send(conn,regis)
		res = b''
		res = res + conn.recv(4096)
		data = json.loads(res)
		logger.debug('res:%s,data:%s' %(res,data))
		mydisconnect(conn)
	except Exception,e:
		traceback.print_exc()
		logger.error('Register to server error.')
		exit()
	res = parse(data)
	if res == 'success':
	#register successfully
		user_thread = threading.Thread(target = user_inter, name = 'User inter')
		user_thread.setDaemon(1)
		user_thread.start()
		logger.info('User inter thread started.')
		
		#Scan thread	
		scan_thread = threading.Thread(target = scan, name = 'Scan thread')
		scan_thread.setDaemon(1)
		scan_thread.start()
		logger.info('Scan thread started.')

		user_thread.join()
		scan_thread.join()
		#uncompleted						
	else:
		logger.error('Server reply a error.')
		exit()

def scan():
	global ip_list
	global result_map
	while True:
		ip_list = []
		result_map = []
		ip_list = get_my_ips()	
		if len(ip_list) == 0:
			continue
		scanner = FtpScanner()
		scanner.set_ip_list(ip_list)
		result_map = scanner.batch_scan2()
		for k,v in result_map.iteritems():
			db = DBOperator()
			db.insert_to_scanned_queue(k,v['info'],v['time'],local_ip)
		#	db.remove_from_allocate_queue(k)	
		for k in result_map.keys():
			db.remove_from_allocate_queue(k)
		#	logger.debug('remove from allocate_queue:%s' %(k))
		logger.info('Finished one loop scan.')

#There are some problems
def user_inter():
	instruction = raw_input()
	if instruction == 'quit()':
		tmp = {}
		tmp['cmd'] = 'del_client'
		tmp['client'] = local_ip
		unregis = pack_data(tmp)
		conn = myconnect(SERVER_ADDR,SERVER_PORT)
		try:
			my_send(conn,unregis)
			res = b''
			res = res + conn.recv(4096)
			data = json.loads(res)
			mydisconnect(conn)
		except Exception,e:
			logger.error('Unregister to server error.')
			exit()
		res = parse(data)
		if res == 'success':
			logger.info('Server reply the close info.')
		else:
			logger.error('Server reply a error.')
		
		logger.info('Close.')
		exit()


def myconnect(server_ip,port):
	try:
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((server_ip,port))
	except socket.error,e:
		traceback.print_exc()
		logger.error('Connect to server error %s.' % (e))
	return s

def mydisconnect(s):
	s.close()

def get_my_ips():
	db = DBOperator()
	ip_list_tmp = db.get_client_ips(local_ip)
	return ip_list_tmp		

def my_send2(conn,data):
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

def my_send(socket,data):
		socket.send(data)

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

def my_recv2():
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
#	a = ['0']*10
	data = json.dumps(data)
#	length3 = len(data)
#	length3 = str(length3)
#	for i in range(len(length3)):
#		a[10-i-1] = length3[len(length3)-i-1]
	res = ""
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


if __name__=='__main__':
	worker()		
