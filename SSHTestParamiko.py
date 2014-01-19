import paramiko

paramiko.util.log_to_file('paramiko.log')
client = paramiko.SSHClient()
rsa_key = paramiko.RSAKey.from_private_key_file('/home/hacker/.ssh/id_rsa',password='password')
#client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#client.connect('127.0.0.1', username='hacker', password='peraspera')
#client.connect('127.0.0.1',key_filename='/home/hacker/.ssh/id_rsa',username='root',password='password')
client.connect('127.0.0.1',pkey=rsa_key,username='root',password='password')
stdout, stdin, stderr = client.exec_command('ls -a')
for line in stdin.readlines():
	print line
client.close()
