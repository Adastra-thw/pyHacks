import paramiko
from paramiko import RSAKey

client = paramiko.SSHClient()
try:
	paramiko.util.log_to_file('paramiko.log')
	rsa_key = paramiko.RSAKey.from_private_key_file('/home/hacker/.ssh/id_rsa',password='password')
	#client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	#client.connect('127.0.0.1', username='hacker', password='peraspera')
	#client.connect('127.0.0.1',key_filename='/home/hacker/.ssh/id_rsa',username='root',password='password')
	client.connect('127.0.0.1',pkey=rsa_key,username='root',password='password')
	sftp = client.open_sftp()
	dirlist = sftp.listdir('.')
	print dirlist
	try:
		sftp.mkdir("demo")
	except IOError:
		print 'IOError, the file already exists!'
	client.close()
except Exception, e:
	print 'Exception %s' % str(e)
	try:
		client.close()
	except:
		pass
