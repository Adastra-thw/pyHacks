import socket
import sys

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

for host in range(10, 12):
	ports = open('ports.txt', 'r')
	vulnbanners = open('vulnbanners.txt', 'r')
	for port in ports:
		try:
			socket.connect(( str(sys.argv[1]+'.'+str(host)), int(port) ))
			print 'Connecting to '+str(sys.argv[1]+'.'+str(host))+' in the port: '+str(port)
			socket.settimeout(1)
			banner = socket.recv(1024)
			for vulnbanner in vulnbanners:
				if banner.strip() in vulnbanner.strip():
					print 'We have a winner! '+banner
					print 'Host: '+str(sys.argv[1]+'.'+str(host))
					print 'Port: '+str(port)
		except :
			print 'Error connecting to: '+str(sys.argv[1]+'.'+str(host)) +':'+ str(port) 
			pass