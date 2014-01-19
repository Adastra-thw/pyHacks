import paramiko
from paramiko import RSAKey
import threading
import socket 
import select

def handleTcpSocket(chan, host, port):
	sock = socket.socket()
	try:
		sock.connect((host, port))
	except Exception, e:
		print('Forwarding request to %s:%d failed: %r' % (host, port, e))
		return
    
	#print('Connected!  Tunnel open %r -> %r -> %r' % (chan.origin_addr, chan.getpeername(), (host, port)))
	while True:
		r, w, x = select.select([sock, chan], [], [])
		if sock in r:
			data = sock.recv(1024)
			if len(data) == 0:
				break
			chan.send(data)
		if chan in r:
			data = chan.recv(1024)
			if len(data) == 0:
				break
			sock.send(data)
	chan.close()
	sock.close()

client = paramiko.SSHClient()
try:
	paramiko.util.log_to_file('paramiko.log')
	rsa_key = paramiko.RSAKey.from_private_key_file('/home/adastra/.ssh/id_rsa',password='password')
	#client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect('127.0.0.1',pkey=rsa_key,username='root',password='password')
	transport = client.get_transport()
	transport.request_port_forward('127.0.0.1', 2222)
	while True:
		chan = transport.accept(1000)
		if chan is None:
		    continue
		thr = threading.Thread(target=handleTcpSocket, args=(chan, '127.0.0.1', 80))
		thr.setDaemon(True)
		thr.start()
	client.close()
except Exception, e:
	print 'Exception %s' % str(e)
	try:
		client.close()
	except:
		pass
