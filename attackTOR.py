from string import lowercase
from plumbum import cli, local
from stem.descriptor.remote import DescriptorDownloader
import logging as log
import nmap

#
#	Attack exit nodes of the TOR Network.
#	Author: Adastra.
#	http://thehackerway.com
#

class Cli(cli.Application):
	verbose = cli.Flag("-v", help="Verbose Mode.")
	brute = cli.Flag(["-b", '--brute'],
					 help="Brute Force Mode. (Specify -u/--users-file and -f/--passwords-file options to select the users and passwords files.)")
	useShodan = cli.Flag(["-s", '--use-shodan'],
						 help="Use ShodanHQ Service. (Specify -k/--shodan-key to set up you shodan key.)")
	threads = 1
	mode = 'win'
	usersFile = None
	passFile = None
	exitNodesToAttack = 10
	shodanKey = None
	scanPorts = "21, 22, 23, 53, 69, 80, 88, 110, 139, 143, 161, 389, 443, 445, 1080, 1433, 3306, 5432, 8080, 9050, 9051, 5800"
	scanProtocol = 'tcp'
	scanArguments = None
	exitNodeFingerprint = None

	@cli.switch(["-n", "--servers-to-attack"], help="Number of TOR exit-nodes to attack.")
	def servers_to_attack(self, exitNodesToAttack):
		self.exitNodesToAttack = exitNodesToAttack

	@cli.switch(["-t", "--threads"], cli.Range(1,20), help='Number of threads to use.')
	def threads(self, threads):
		self.threads = threads

	@cli.switch(["-m", "--mode"],cli.Set("windows", "linux", case_sensitive = False), mandatory=True, help="Filter the platform of exit-nodes to attack.") 
	def server_mode(self, mode):
		self.mode = mode

	@cli.switch(["-u", "--users-file"], help="Users File in the Bruteforce mode.", requires = ["--brute"]) 
	def users_file(self, usersFile):
		self.usersFile = usersFile

	@cli.switch(["-f", "--passwords-file"], help="Passwords File in the Bruteforce mode.", requires = ["--brute"]) 
	def users_file(self, usersFile):
		self.usersFile = usersFile

	@cli.switch(["-k", "--shodan-key"], help="Development Key to use Shodan API.", requires = ["--use-shodan"]) 
	def shodan_key(self, shodanKey):
		self.shodanKey = shodanKey

	@cli.switch(["-l", "--list-ports"], str, help="Comma-separated List of ports to scan with Nmap.") 
	def list_ports(self, scanPorts):
		self.scanPorts = scanPorts

	@cli.switch(["-p", "--scan-protocol"], cli.Set("tcp", "udp", case_sensitive = True), help="Protocol used to scan the target.") 
	def scan_protocol(self, scanProtocol):
		self.scanProtocol = scanProtocol

	@cli.switch(["-a", "--scan-arguments"], help="Arguments to Nmap.") 
	def scan_arguments(self, scanArguments):
		self.scanArguments = scanArguments

	@cli.switch(["-e", "--exit-node-fingerprint"], help="ExitNode's Fingerprint to attack.") 
	def exitNodeFingerprint(self, exitNodeFingerprint):
		self.exitNodeFingerprint = exitNodeFingerprint



	def main(self):
		attack = MainAttack(self)
		attack.listExitNodes()


class MainAttack:
	exitNodes = []
	cli = None
	scan = None
	def __init__(self, cli):
		self.cli = cli
		if self.cli.verbose:
			log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
			log.info("[+] Verbose mode activated.")
		else:
			log.basicConfig(format="%(levelname)s: %(message)s")

	def listExitNodes(self):
		log.info("[+] Try to listing the current Exit-Nodes of TOR.")
		if cli.exitNodeFingerprint != None:
			log.info("[+] Using the fingerprint: %s " %(cli.exitNodeFingerprint))
		log.info("[+] Filter by platform: %s." %(self.cli.mode))
		downloader = DescriptorDownloader()
		for descriptor in downloader.get_server_descriptors().run():
            if descriptor.exit_policy.is_exiting_allowed() and lowercase(self.cli.mode) in lowercase(descriptor.operating_system):
                log.info("[+] %s System found... Nickname: %s - OS Version: %s" %(self.cli.mode, descriptor.nickname, descriptor.operating_system))
                log.info("[+] Starting the NMap Scan with the following options: ")
                log.info("[+][+] Scan Address: %s " %(descriptor.address))
                log.info("[+][+] Scan Arguments: %s " %(self.cli.scanArguments))
                log.info("[+][+] Scan Ports: %s " %(self.cli.scanPorts))
                nm = nmap.PortScanner()
                scan = nm.scan(descriptor.address, self.cli.scanPorts, arguments=self.cli.scanArguments)
                self.recordNmapScan(scan)
                log.info('[+] Scan Ended for %s .' %(descriptor.nickname))

    def recordNmapScan(self, scan):
		entryFile = 'nmapScan.txt'
		nmapFileResults = open(entryFile, 'w')
		entry = '------- NMAP SCAN REPORT -------'
		for host in scan.keys():
			entry += 'Host: %s Hostname: %s \n' %(host, scan[host].hostname())
			entry += 'State: %s \n' %(scan[host]['status'])
			mapPorts = scan[host][self.cli.scanProtocol].keys()
			for port in mapPorts:
				entry += 'Port: %s \n' %(port)
				entry += 'State: %s \n ' %(scan[host][self.cli.scanProtocol][port]['state'])
				entry += 'Reason: %s \n ' %(scan[host][self.cli.scanProtocol][port]['reason'])
				entry += 'Name: %s \n ' %(scan[host][self.cli.scanProtocol][port]['name'])

		nmapFileResults.write(entry)
		nmapFileResults.close()

if __name__ == "__main__":
	Cli.run()

#Try to find and attack windows.
#Try to find and attack Linux.
