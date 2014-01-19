from plumbum import cli, local

class ServidorTest(cli.Application):
	verbose = cli.Flag("-v", help = "Arrancar el servidor en Verbose mode")
	port = 8080 # Puerto por defecto
	mode = "TCP" #Protocolo de red por defecto
	type = "HTTP" 

	@cli.switch(["-p", "--port"], cli.Range(1024,65535)) #Puerto entre 1024 y 65535
	def server_port(self, port):
		self.port = port

	@cli.switch(["-m", "--mode"],cli.Set("TCP", "UDP", case_sensitive = False)) #Protocolo de red (TCP o UDP)
	def server_mode(self, mode):
		self.mode = mode
		
	@cli.switch(["-t", "--type"], cli.Set("HTTP", "HTTPS", case_sensitive = False)) 
	def server_type(self, type):
		self.type = type
		
	def main(self):
		print self.port, self.mode, self.type, self.verbose

if __name__ == "__main__":
	ServidorTest.run()
