from fabric.api import local, run, env, hosts

#env.hosts = ['localhost']

@hosts('192.168.1.219')
def uname():
	#local('ifconfig')
	run('uname -a')

@hosts('localhost')
def w():
	run('w')
