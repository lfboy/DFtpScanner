#!/usr/bin/python
import os
import sys
import ConfigParser
import tools
import socket
import json
import threading
import thread
import datetime
import time
from DBOperator import DBOperator

config_file = os.getcwd() + '/config.ini'
cf = ConfigParser.ConfigParser()
cf.read(config_file)
MIN_CLIENTS = int(cf.get('server','min_clients'),10)
TIMEOUT = int(cf.get('server','timeout'),10)
PORT = int(cf.get('server','port'),10)
IP_STEP = int(cf.get('server','step'),10)
INTERVAL = int(cf.get('server','interval'),10)
LOG_FILE = os.path.join(os.getcwd(),cf.get('support','log_file'))
logger = tools.set_logger('master3.py',LOG_FILE)

def master():
	global str_ip_start 
	str_ip_start = sys.argv[1]
	global str_ip_end 
	str_ip_end = sys.argv[2]
	global client_list 
	client_list = []
	global client_num 
	client_num = 0

	global t 
	t = threading.Thread(target = serv, name = 'listener')
	t.setDaemon(1)
	t.start()
	logger.info('Start listen thread.')

	global t2 
	t2 = threading.Thread(target = allocate, name = 'allocate_ips')
	t2.setDaemon(1)
	t2.start()	

	user_inter()
	t.join()
	t2.join()

def user_inter():
	instruction = raw_input()
	if instruction == 'quit()':
		logger.info('Master close.')
		exit(0)

def allocate():

	ip_start = tools.ip2long(str_ip_start)
	ip_end = tools.ip2long(str_ip_end)
	i = 0
	if ip_start > ip_end:
		logger.error('Invalid ip range.')
		return
	 
	while ip_end - ip_start > IP_STEP:
		records = DBOperator().get_allocate_queue_record_amount()
		if records < client_num*IP_STEP*2 and client_num > 0:
			#Insert allocate_queue
			ip_list = generate_ips2(ip_start,ip_start+IP_STEP+1)
			insert_ips_to_allocate(ip_list,client_list[i])
			logger.info('%s - %s allocated to %s.'%(ip_list[0],ip_list[-1],client_list[i]))
			i = (i+1) % client_num
			ip_start += IP_STEP
		else:
		   time.sleep(INTERVAL)	
		   continue
	
	while ip_end - ip_start > 0:
		records = DBOperator().get_allocate_queue_record_amount()
		if records < client_num*IP_STEP*2 and client_num > 0:
			#Insert allocate_queue
			ip_list = generate_ips2(ip_start,ip_end+1)
			insert_ips_to_allocate(ip_list,client_list[i])
			logger.info('%s - %s allocated to %s.'%(ip_list[0],ip_list[-1],client_list[i]))
			i = (i+1) % client_num
			ip_start = ip_end
		else:
		   time.sleep(INTERVAL)	
		   continue

	

def serv():
#	TIMEOUT = 60
#	PORT = 6600
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
			thread.start_new_thread(my_recv,c)
		except:
			logger.info('Time out.')
			continue
def my_recv(socket):
	while True:
		try:
			a = self.socket.recv(10)
			length = string.atoi(a)
			logger.info('DataLength: %d' % length)
			res = b''
			while len(res) < length:
				res = res + socket.recv(4096)
			data = json.loads(res)
			cmd = data['cmd'] 
		except:
			logger.error('Receive Error.')
			return
		
		res = parse(data)
		if len(res) > 0:
			status = res['status']
			socket.send(packet_data[res])	

def pack_data(response):
	a = ['0']*10
	data = json.dumps(data)
	length = len(data)
	length = str(length)
	for i in range(len(length)):
		a[10-i-1] = length[len(length)-i-1]
	res = "".join(a)
	res = res + data
	logger.debug('Send info is :' + res)
	return res

def parse(data):
	logger.debug('Received data is :' + data)
	cmd = data['cmd']
	if cmd == 'add_client':
		client = data['ip']
		add_client(client)
		result = {'cmd':'add_client','result':'success'}
	elif cmd == 'del_client':
		client = data['ip']
		del_client(client)
		result = {'cmd':'del_client','result':'success'}
	return result

def add_client(client):
	client_list.insert(client)
	client_num = client_num + 1
def del_client(client):
	client_list.remove(client)
	client_num = client_num - 1

if __name__=="__main__":
	try:
		master()
	except Exception,e:
		print e	
