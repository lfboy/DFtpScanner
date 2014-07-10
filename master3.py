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
import traceback
import string
from DBOperator import DBOperator

config_file = os.getcwd() + '/config.ini'
cf = ConfigParser.ConfigParser()
cf.read(config_file)
MIN_CLIENTS = int(cf.get('server','min_clients'),10)
TIMEOUT = int(cf.get('server','timeout'),10)
HOST = cf.get('server','ip')
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
#	global client_num 
#	client_num = 0
	global start_time
	start_time = tools.get_current_time()
	global end_time
		

	global t1 
	t1 = threading.Thread(target = serv, name = 'serv thread')
	t1.setDaemon(1)
	t1.start()
	logger.info('Start serv thread.')

	global t2 
	t2 = threading.Thread(target = allocate, name = 'allocate_ips')
	t2.setDaemon(1)
	t2.start()	
	logger.info('Start allocate thread.')	

	user_inter()
	t1.join()
	t2.join()

	
def user_inter():
	while True:
		instruction = raw_input()
		if instruction == 'quit()':
			logger.info('Master close.')
			exit(0)

def allocate():
	ip_start = tools.ip2long(str_ip_start)
	ip_end = tools.ip2long(str_ip_end)
#	client_num = len(client_list)
	i = 0
	if ip_start > ip_end:
		logger.error('Invalid ip range.')
		return
	hosts = ip_end - ip_start + 1	 

	while ip_end - ip_start > IP_STEP:
		client_num = len(client_list)
		if client_num <= 0:
			time.sleep(INTERVAL)
			continue		
		records = DBOperator().get_client_allocated_amount(client_list[i])
		logger.debug('Records amount %d, client num %d.' % (records,client_num))
		if records < IP_STEP*2:
			#Insert allocate_queue
			ip_list = tools.generate_ips2(ip_start,ip_start+IP_STEP)
			DBOperator().insert_ips_to_allocate(ip_list,client_list[i])
			logger.info('%s - %s allocated to %s.'%(ip_list[0],ip_list[-1],client_list[i]))
			i = (i+1) % client_num
			ip_start += IP_STEP
		else:
		   time.sleep(INTERVAL)	
		   i = (i+1)%client_num
		   continue
	
	while ip_end - ip_start > 0:
		records = DBOperator().get_allocate_queue_record_amount()
		if records < client_num*IP_STEP*2 and client_num > 0:
			#Insert allocate_queue
			ip_list = tools.generate_ips2(ip_start,ip_end+1)
			DBOperator().insert_ips_to_allocate(ip_list,client_list[i])
			logger.info('%s - %s allocated to %s.'%(ip_list[0],ip_list[-1],client_list[i]))
			i = (i+1) % client_num
			ip_start = ip_end
		else:
		   time.sleep(INTERVAL)	
		   continue
	end_time = tools.get_current_time()
	print 'Time:%s , %s, Hosts: %d' %(start_time,end_time,hosts)	

def serv():
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	s.bind((HOST,PORT))
	s.listen(5)
	while True:
		logger.info('Ready to connect!')
		try:
			c,addr = s.accept()
			logger.info('Got guest from %s' % (addr[0]) )
	#		print 'Got guest from ',addr
			thread.start_new_thread(my_recv,(c,))
		except:
			traceback.print_exc()
			logger.info('Time out.')
			continue

def my_recv(socket2):
	socket = socket2
	try:
		res = b''
		res = res + socket.recv(4096)
		data = json.loads(res)
	except:
		traceback.print_exc()
		logger.error('Receive error.')
	
	res = parse(data)
	if len(res) > 0:
#		status = res['result']
		socket.send(pack_data(res))	

def pack_data(data):
	data = json.dumps(data)
	res = ""
	res = res + data
	logger.debug('Send info is :' + res)
	return res

def parse(data):
	logger.debug('Received data is :' + str(data))
	cmd = data['cmd']
	if cmd == 'add_client':
		client = data['client']
		add_client(client)
		result = {'cmd':'add_client','result':'success'}
	elif cmd == 'del_client':
		client = data['client']
		del_client(client)
		result = {'cmd':'del_client','result':'success'}
	return result

def add_client(client):
	client_list.append(client)

def del_client(client):
	client_list.remove(client)

if __name__=="__main__":
	try:
		master()
	except Exception,e:
		print e	
