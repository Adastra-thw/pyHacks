from shodan.api import WebAPIError
import zlib
from shodan import WebAPI
from stem.descriptor import parse_file
from plumbum import cli, local
from stem.descriptor.remote import DescriptorDownloader
import logging as log
import threading
import nmap
import Queue
from time import gmtime, strftime

#
#	Attack exit nodes of the TOR Network.
#	Author: Adastra.
#	http://thehackerway.com
#

class Cli(cli.Application):
	'''
		Command-Line options received.
	'''
	verbose = cli.Flag(["-v", '--verbose'], help="Verbose Mode.")
	brute = cli.Flag(["-b", '--brute'], help="Brute Force Mode. (Specify -u/--users-file and -f/--passwords-file options to select the users and passwords files.)")
	useMirror = cli.Flag(["-d", '--use-mirrors'], help="Use the mirror directories of TOR. This will help to not overwhelm the official directories")
	useShodan = cli.Flag(["-s", '--use-shodan'], help="Use ShodanHQ Service. (Specify -k/--shodan-key to set up the file where's stored your shodan key.)")
	threads = 1
	mode = None
	usersFile = None
	passFile = None
	exitNodesToAttack = 10 #Number of default exit-nodes to filter from the Server Descriptor file.
	shodanKey = None
	scanPorts = "21,22,23,53,69,80,88,110,139,143,161,389,443,445,1079,1080,1433,3306,5432,8080,9050,9051,5800" #Default ports used to scan with nmap.
	scanProtocol = 'tcp' #Using TCP protocol to perform the nmap scan.
	scanArguments = None #Scan Arguments passed to nmap.
	exitNodeFingerprint = None #Fingerprint of the exit-node to attack.
	queue = Queue.Queue() #Queue with the host/open-port found in the scanning. 

	@cli.switch(["-n", "--servers-to-attack"], int, help="Number of TOR exit-nodes to attack. Default = 10")
	def servers_to_attack(self, exitNodesToAttack):
		'''	
			Number of "exit-nodes" to attack received from command-line
		'''
		self.exitNodesToAttack = exitNodesToAttack

	@cli.switch(["-t", "--threads"], cli.Range(1, 20), help='Number of threads to use.')
	def number_threads(self, threads):
		'''	
			Number of threads to create when the scanning process has been done.
		'''
		self.threads = threads

	@cli.switch(["-m", "--mode"], cli.Set("windows", "linux", case_sensitive=False), mandatory=True, help="Filter the platform of exit-nodes to attack.")
	def server_mode(self, mode):
		'''
			Server Mode: Search for Windows or Linux machines.
		'''
		self.mode = mode

	@cli.switch(["-u", "--users-file"], help="Users File in the Bruteforce mode.", requires=["--brute"])
	def users_file(self, usersFile):
		'''
			User's file. Used to perform bruteforce attacks.
		'''	
		self.usersFile = usersFile

	@cli.switch(["-f", "--passwords-file"], help="Passwords File in the Bruteforce mode.", requires=["--brute"])
	def users_file(self, usersFile):
		'''
						User's file. Used to perform bruteforce attacks.		
		'''
		self.usersFile = usersFile

	@cli.switch(["-k", "--shodan-key"], str, help="Development Key to use Shodan API.", requires=["--use-shodan"])
	def shodan_key(self, shodanKey):
		'''
			This option is used to specify the file where the shodan development key is stored
		'''
		self.shodanKey = shodanKey

	@cli.switch(["-l", "--list-ports"], str, help="Comma-separated List of ports to scan with Nmap. Don't use spaces")
	def list_ports(self, scanPorts):
		'''
			List of ports used to perform the nmap scan.
		'''
		self.scanPorts = scanPorts

	@cli.switch(["-p", "--scan-protocol"], cli.Set("tcp", "udp", case_sensitive=True), help="Protocol used to scan the target.")
	def scan_protocol(self, scanProtocol):
		'''
			Protocol used to perform the nmap scan.
		'''
		self.scanProtocol = scanProtocol

	@cli.switch(["-a", "--scan-arguments"], str, help='Arguments to Nmap. Use "" to specify the arguments. For example: "-sSV -A -Pn"')
	def scan_arguments(self, scanArguments):
		'''
			Arguments used to perform the nmap scan.
		'''
		self.scanArguments = scanArguments

	@cli.switch(["-e", "--exit-node-fingerprint"], str, help="ExitNode's Fingerprint to attack.")
	def exitNode_Fingerprint(self, exitNodeFingerprint):
		'''
			If we want to perform a single attack against an known "exit-node", We can specify the fingerprint of the exit-node to perform the attack.
		'''
		self.exitNodeFingerprint = exitNodeFingerprint

	def main(self):
		'''
			List and Scan the exit nodes. The function will return an dictionary with the exitnodes found and the open ports.
			THIS PROCESS IS VERY SLOW AND SOMETIMES THE CONNECTION WITH THE DIRECTORY AUTHORITIES IS NOT AVAILABLE.
		'''
		discovery = Discovery(self)
		exitNodes = discovery.listExitNodes() #Returns a tuple with IP Addresses and open-ports.
		if exitNodes != None and len(exitNodes) > 0:
			for thread in range(self.threads): #Creating the number of threads specified by command-line.
				worker = WorkerThread(self.queue, thread, self)
				worker.setDaemon(True)
				worker.start()

			for exitNode in exitNodes.items():
				self.queue.put(exitNode)
			self.queue.join() #Blocks the main process until the queue is empty.

		log.info("[+] Process finished at "+ strftime("%Y-%m-%d %H:%M:%S", gmtime()))

class Discovery:
	'''
		Class used to list the current "exit-nodes" from the TOR network and perform the nmap scanning to discover the open ports.
	'''
	exitNodes = {}
	cli = None
	scan = None

	def __init__(self, cli):
		self.cli = cli
		if self.cli.verbose:
			log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
			log.info("[+] Verbose mode activated.")
		else:
			log.basicConfig(format="%(levelname)s: %(message)s")
		log.info("[+] Process started at "+ strftime("%Y-%m-%d %H:%M:%S", gmtime()))

	def listExitNodes(self):
		'''
			List the Exit Nodes using the filters specified by command-line.
		'''
		nodesAlreadyScanned = []
		log.info("[+] Try to listing the current Exit-Nodes of TOR.")
		if self.cli.exitNodeFingerprint != None:
			log.info("[+] Using the fingerprint: %s " % (self.cli.exitNodeFingerprint))
		log.info("[+] Filter by platform: %s." % (self.cli.mode))
		log.info("[+] Retrieving the first %d records in the Descriptors." %(self.cli.exitNodesToAttack))
		
		if self.cli.useMirror == True:
			log.info("[+] Using the Directory Mirrors to get the descriptors")
		downloader = DescriptorDownloader(use_mirrors=self.cli.useMirror)
		nm = nmap.PortScanner()
		if self.cli.exitNodeFingerprint != None:
			descriptors = downloader.get_server_descriptors(fingerprints=[self.cli.exitNodeFingerprint])
		else:
			descriptors = downloader.get_server_descriptors()
		try:
			listDescriptors = descriptors.run()
		except zlib.error:
			log.error("[-] Error fetching the TOR descriptors. This is something quite common... Try again in a few seconds.")
			return				
		log.info("[+] Number of Records found: %d " %(len(listDescriptors)))		
		for descriptor in listDescriptors[1:self.cli.exitNodesToAttack]:
		#for descriptor in parse_file(open("/home/adastra/Escritorio/tor-browser_en-US-Firefox/Data/Tor/cached-consensus")):
			if self.cli.mode.lower() in descriptor.operating_system.lower() and descriptor.exit_policy.is_exiting_allowed():
				#SEARCH FILTERING BY FINGERPRINT
				#Conditions: Fingerprint specified in command-line AND
				#	 Relay Fingerprint equals to the Fingerprint specified in command-line. AND 
				#	 Relay's Operative System equals to the Operative System (option mode) specified in command-line AND
				#	 The Relay is a Exit Node. 	
				if descriptor.address not in nodesAlreadyScanned:
					log.info("[+] %s System has been found... Nickname: %s - OS Version: %s" % (descriptor.operating_system, descriptor.nickname, descriptor.operating_system))
					log.info("[+] Starting the NMap Scan with the following options: ")
					log.info("[+][+] Scan Address: %s " % (descriptor.address))
					log.info("[+][+] Scan Arguments: %s " % (self.cli.scanArguments))
					log.info("[+][+] Scan Ports: %s " % (self.cli.scanPorts))
					if self.cli.scanArguments != None:
						nm.scan(descriptor.address, self.cli.scanPorts, arguments=self.cli.scanArguments)
					else:
						nm.scan(descriptor.address, self.cli.scanPorts)	
					self.recordNmapScan(nm)
					log.info('[+] Scan Ended for %s .' % (descriptor.nickname))
					nodesAlreadyScanned.append(descriptor.address)

		if len(self.exitNodes) == 0:
			log.info("[+] In the first %d records searching for the %s Operating System, there's no results (machines with detected open ports)" %(self.cli.exitNodesToAttack, self.cli.mode.lower()))	
		return self.exitNodes

	def recordNmapScan(self, scan):
		'''
			Performs the NMap scan using python-nmap library.
			Returns the exitnodes with the open ports found in the scanning process.
		'''
		entryFile = 'nmapScan.txt'
		nmapFileResults = open(entryFile, 'a')

		for host in scan.all_hosts():
			entry = '------- NMAP SCAN REPORT START FOR %s------- \n' %(host)
			entry += '[+] Host: %s \n' % (host)
			if scan[host].has_key('status'):
				entry += '[+][+]State: %s \n' % (scan[host]['status']['state'])
				entry += '[+][+]Reason: %s \n' % (scan[host]['status']['reason'])
			if scan[host].has_key(self.cli.scanProtocol):
				mapPorts = scan[host][self.cli.scanProtocol].keys()
				for port in mapPorts:
					entry += 'Port: %s \n' % (port)
					entry += 'State: %s \n ' % (scan[host][self.cli.scanProtocol][port]['state'])
					if 'open' in (scan[host][self.cli.scanProtocol][port]['state']):
						self.exitNodes[host] = port
					if scan[host][self.cli.scanProtocol][port].has_key('reason'):
						entry += 'Reason: %s \n ' % (scan[host][self.cli.scanProtocol][port]['reason'])
					if scan[host][self.cli.scanProtocol][port].has_key('name'):
						entry += 'Name: %s \n ' % (scan[host][self.cli.scanProtocol][port]['name'])
			else:
				log.info("[-] There's no match in the Nmap scan with the specified protocol %s" %(self.cli.scanProtocol))
			entry += '------- NMAP SCAN REPORT END ------- \n'
			entry += '\n\n'
			nmapFileResults.write(entry)
		nmapFileResults.close()

class WorkerThread(threading.Thread):
	'''
	Worker Thread to information gathering and attack the exit nodes found.
	'''
	
	def __init__(self, queue, tid, cli) :
		threading.Thread.__init__(self)
		self.queue = queue
		self.tid = tid
        	self.cli = cli
		self.bruteForcePorts ={'ftpBrute':21, 'sshBrute':22}
		if self.cli.useShodan == True:
			#Using Shodan to search information about this machine in shodan database.
			log.info("[+] Shodan Activated. About to read the Development Key. ")
			if self.cli.shodanKey == None:
				#If the key is None, we can't use shodan.
				log.warn("[-] Shodan Key's File has not been specified. We can't use shodan without a valid key")
			else:
				#Read the shodan key and create the WebAPI object.
				shodanKey = open(self.cli.shodanKey).readline().rstrip('\n')
				self.shodanApi = WebAPI(shodanKey)
				log.info("[+] Connected to Shodan. ")
	def run(self) :
		lock = threading.Lock()
		while True :
			lock.acquire()
			host = None
			try:
				ip, port = self.queue.get(timeout=1)
				if hasattr(self, 'shodanApi'):
					log.info("[+] Using Shodan against %s " %(ip))
					try:
						shodanResults = self.shodanApi.host(ip)
						recordShodanResults(self, ip, shodanResults)
					except WebAPIError:
						log.error("[-] There's no information about %s in the Shodan Database." %(ip))
						pass
				
				if self.cli.brute == True:
					if self.cli.usersFile != None and self.cli.passFile != None:
						for method in self.bruteForcePorts.keys():
							if self.bruteForcePorts[method] == port:
								#Open port detected for a service supported in the "Brute-Forcer"
								#Calling the method using reflection.
								attr(service)
								
					else:
						log.warn("[-] BruteForce mode specified but there's no files for users and passwords. Use -u and -f options")
			except Queue.Empty :
				log.info("Worker %d exiting... "%self.tid)
			finally:
				log.info("Releasing the Lock in the Thread %d "%self.tid)
				lock.release()
				self.queue.task_done()
	
	def ftpBrute(self):
		log.info("Starting FTP BruteForce mode on Thread: %d "%self.tid)
		#log.info("Reading the Users File: %s "%self.cli.)
		
	def sshBrute(self):
		log.info("Starting SSH BruteForce mode on Thread: %d "%self.tid)
	
	def recordShodanResults(self, host, results):
		entryFile = 'shodanScan-%s.txt' %(host)
		shodanFileResults = open(entryFile, 'a')
		entry = '------- SHODAN REPORT START FOR %s ------- \n' %(host)
		recursiveInfo(entry, results)		
		entry = '------- SHODAN REPORT END FOR %s ------- \n' %(host)
		shodanFileResults.write(entry)
		shodanFileResults.close()			

	def recursiveInfo(self, entry, data):
		if type(data) == dict:
			for key in results.keys():
				if type(key) == dict:
					entry += recursiveInfo(entry, key)
				elif type(key) == list:
					for element in key:
						if type(key) == dict:
							entry += recursiveInfo(entry, key)
											
				else:
					entry += '[+]%s : %s \n' %(key, results[key])
					print entry
	
if __name__ == "__main__":
	'''
		Start the main program.
	'''
	Cli.run()
