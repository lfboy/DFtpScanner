#!/usr/bin/python
import logging
import socket,struct

def set_logger(program,log_file):
	logger = logging.getLogger(program)
	logger.setLevel(logging.DEBUG)
	
 	fh = logging.FileHandler(log_file)
	fh.setLevel(logging.WARN)

	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)

	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
	ch.setFormatter(formatter)
	fh.setFormatter(formatter)
	logger.addHandler(ch)
	logger.addHandler(fh)

	return logger

def ip2long(str_ip):
	packedIP = socket.inet_aton(str_ip)
	return struct.unpack('!L',packedIP)[0]

def long2ip(num_ip):
	ip = socket.inet_ntoa(struct.pack('I',socket.htonl(num_ip)))
	return ip	

def generate_ips(start_str,end_str):
	ip_list=[]
	start_num  = ip2long(start_str)
	end_num = ip2long(end_str)
	if start_num > end_num:
		return ip_list
	for i in range(start_num,end_num+1):
		ip = long2ip(i)
		ip_list.append(ip)
	return ip_list

if __name__=='__main__':
	start = raw_input('Start:')
	end = raw_input('End:')
	lists = generate_ips(start,end)
	for i in lists:
		print i	
