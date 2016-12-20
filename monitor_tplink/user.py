#!/usr/bin/python
# coding=utf-8
import time
import urllib2, base64
import requests

global_dict = {
		"00-08-00-DE-08-1A" : "mother_phone",
		"00-03-44-0C-07-3A" : "father_phone",
		"00-0B-32-0B-00-99" : "my_phone",
		"00-0B-32-AB-10-19" : "my_ipad",
		"00-0B-32-AB-20-19" : "brother_phone",
		"00-0B-C2-AB-20-19" : "brother_ipad",
		"00-0B-32-0B-00-19" : "xiaomi"
	}

def handle_mac2name(string_mac):
	#strip "
	ret_string = global_dict.get(string_mac.replace('"',''), "other")
	return ret_string


def handle_write_file(string):
	file_object = open('user.txt', 'aw+')
	try:
		file_object.write(string)
	finally:
		file_object.close()


def handle_hostarray2string(string_array):

	write_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

	for i in range(0, len(string_array)):
		string = string_array[i]
		if 0 == i%7: 
			return_string = handle_mac2name(string)
			write_string += "\n" + return_string + "\t\t" + string;
		else:
			write_string += "\t\t" + string;

	write_string += "\n"
	return write_string

	handle_write_file(string)
			 
	
def get_hostlist_array():
	hostarray = []
	string_find = 'var hostList'
	host = '####my_tplink_ip###'
	url = 'http://' + host + '/userRpm/WlanStationRpm.htm'

	username = "admin"
	password = "####my_tplink_login_password####"
	base64_cookie = base64.b64encode(username + ":" + password)
	cookie = { "Authorization":"Basic " + base64_cookie }

	referer = 'http://' + host + '/userRpm/MenuRpm.htm'
	headers = {
		'Host': host,
		'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
		'Referer' : referer,
        }
	try:
		response = requests.get(url = url, headers = headers, cookies = cookie)
		content = response.content
		hostlist_head_index = content.find(string_find)
		hostlist_string_head = content[hostlist_head_index : ]	
		
		hostlist_tail_index = hostlist_string_head.find(';')
		hostlist_string = hostlist_string_head[0 : hostlist_tail_index]	

		# strip "var hostList" and "0 0)" line
		hostarray = hostlist_string.replace(',', '').split('\n')[1:-1]
	except Exception,e:
		write_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\t" + "exception" + "\n"
		handle_write_file(string)

	return hostarray

if __name__ == '__main__':
	while True:
		time.sleep(180)
		hostarray = get_hostlist_array()				
		if 0 == len(hostarray):
			continue

		string = handle_hostarray2string(hostarray)
		handle_write_file(string)
