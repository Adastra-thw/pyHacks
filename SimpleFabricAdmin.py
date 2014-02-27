from fabric.api import env, run, run, execute, hide, sudo, open_shell
import sys

def execCommand(command):
	try:
		with hide('running', 'stdout', 'stderr'):
			if command.strip()[0:5] == "sudo":
				results = sudo(command)
			else:
				results = run(command)
	except:
		results = "Unexpected error:", sys.exc_info()[0]		
	return results


if __name__ == "__main__":
	machines = open('machines.txt', 'r')
	if len(sys.argv) != 2:
		print "usage: python SimpleFabricAdmin.py <command>"
		exit()

	for line in machines.readlines():
		if line == '\n':
			continue
		host = line.split(":")[0]
		user = line.split(":")[1]
		password = line.split(":")[2]
		port = line.split(":")[3].rstrip('\n')	
		hostString = user+"@"+host+":"+port
		env.hosts.append(hostString)
		env.passwords[hostString] = password
	for host, output in execute(execCommand, sys.argv[1], hosts=env.hosts).iteritems():
		print "Host: "+host
		print " output: "+str(output)
