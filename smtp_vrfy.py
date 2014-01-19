#!/usr/bin/python
import socket
import sys
if len(sys.argv) != 8:
         print "Usage: smtpCheck.py initRange maxRange ipSegAddress ipPort smtpMethod usernamesFile outputFile\n"
         print "Example: python smtpCheck.py 200 255 192.168.17 25 VRFY dict.txt smtpOutput.txt"
         print "Example: python smtpCheck.py 200 255 192.168.17 25 EXPN dict.txt smtpOutput.txt"
         print "Example: python smtpCheck.py 200 255 192.168.17 25 RCPT TO: dict.txt smtpOutput.txt"
         sys.exit(0)
initRange = int(sys.argv[1])
maxRange = int(sys.argv[2])
ipSegAddress = sys.argv[3]
ipPort = int(sys.argv[4])
smtpMethod = sys.argv[5]
usersFile = sys.argv[6]
outputFileName = sys.argv[7]
results=''
validUsers=''
for ipAddress in range(initRange, maxRange):
        try:
                 s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                 s.settimeout(5)
                 ip = ipSegAddress+'.'+str(ipAddress)
                 print ip
                 connect = s.connect((ip,ipPort))
                 # Receive the banner
                 banner=s.recv(1024)
                 print banner
                 s.settimeout(15)
                 results = results+'\n'+ip+' - '+banner
		 if '220' in banner:
                 	with open(usersFile, 'r') as f:
                        	for user in f:
                                	s.send(smtpMethod+' '+user)
                                        result=ip+' '+s.recv(1024)
                                        print result
					if '252' in result:
                                        	validUsers += result
                          	f.close()
                 # Close the socket
                 s.close()
        except socket.timeout:
                 results = results+'Timeout for : '+ip+'\n'
                 print 'Timeout for : '+ip
                 continue
        except socket.error:
                 print 'Connection error '+ip
                 continue
with open(outputFileName, 'w') as fw:
        fw.write(validUsers)
        fw.close

