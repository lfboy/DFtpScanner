#!/usr/bin/python
import logging
import socket,struct
import fcntl

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

def generate_ips2(start,end):
	ip_list=[]
	if start > end:
		return ip_list
	for i in range(start,end):
		ip = long2ip(i)
		ip_list.append(ip)
	return ip_list

def get_local_ip(ifname):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s',ifname[:15]))[20:24])

if __name__=='__main__':
	start = raw_input('Start:')
	end = raw_input('End:')
	lists = generate_ips(start,end)
	for i in lists:
		print i	
