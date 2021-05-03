"""
Port Scanner

This python script file is the Port Scanner tool, which serves the purpose of scanning all the ports of a specified target server. And, then it checks wheter all the ports from 1 to 65,535 are open or closed. After the scan is completed, then the script lists all the open ports of the specified target server on the console screen. The port scanner can be used to detect the open ports of a web server / proxy server whom we either wanna get authorized/unauthorized access to. The tool's legality of usage depends upon which type of targets are you using on. If you are using this tool with a target web server on which you don't have any authorization, then your ass might be landing behind the bars. For a lil dark information, this tool will detect the open ports on the servers, and then we can easily DDOS attack or SSH bruteforce attack on those open ports to hack into the target server. This tool can be said to be a part of information gathering tool or a forensic tool. This tool is made for those who want to learn the darkside of python and programming, where we learn to exploit a computer system's security and programming. The tool is made for hackers who want to test their web servers and improve security of it. To use this tool, use this command on the terminal : 'python3 portscanner.py <website-link of target>' or 'python3 portscanner.py <ip-address of the target web server>'.
Author : 
Created on : 

Last modified by : Rishav Das (https://github.com/rdofficial/)
Last modified on : May 3, 2021

Changes made in last modification :
1. Updated the entire structure of the code, and made it more beautiful + more fluent for code readers.
2. Added more code for error free execution of the tool.
3. Added the feature of detecting each port and telling the user wheter open or closed. Finally, displaying all the open ports on the specified target server.
4. Added commented docs for making the script look more professional.
5. Removed the pyfiglet depedency, instead added colored output on console feature for linux computers.

Authors contributed to this script (Add your name below if you have contributed) :
1. 
2. Rishav Das (github:https://github.com/rdofficial/, email:rdofficial192@gmail.com)
"""

# Importing the required functions and modules
try:
    from sys import argv, platform
    import socket 
    from datetime import datetime 
except Exception as e:
    # If there are any errors encountered during the importing of the modules, then we display the error message on the console screen

    print('[ Error : {} ]'.format(e))

# Defining the ANSII color codes variables
if 'linux' in platform:
    # If the operating system type is linux, then only we define the color variables

    red = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    blue = '\033[94m'
    red_rev = '\033[07;91m'
    yellow_rev = '\033[07;93m'
    defcol = '\033[00m'
else:
    # If the operating system type is not linux, then we leave the color variables blank

    red = ''
    green = ''
    yellow = ''
    blue = ''
    red_rev = ''
    yellow_rev = ''
    defcol = ''

try:
    # Displaying the heading of the script on the console screen
    print('\t{yellow_rev}[ PORT SCANNER ]{defcol}'.format(yellow_rev = yellow_rev, defcol = defcol))
       
    # Defining a target 
    if len(argv) == 2:
        # If the user entered argument for the target hostname, then we continue to translate hostname to IPv4 

        target = socket.gethostbyname(argv[1])  
    else:
        # If the user does not enters the argument for target hostname, then we display the error message on the console screen

        print(red_rev + '[ Error : Invalid amount of arguments, target hostname required ]' + defcol)

    # Displaying the status of the target on the console screen
    print('-' * 50)
    print('[{}${}] Scanning target : '.format(yellow, defcol) + green + target + defcol)
    print('[{}${}] Scanning started at : '.format(yellow, defcol) + blue + str(datetime.now()) + defcol)
    print('-'* 50)
       
    # A array which will contain the list of open ports
    openPorts = []

    # We will scan ports between 1 to 65,535
    for port in range(1, 65535):
        # Scanning the ports in a loop

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        socket.setdefaulttimeout(1) 
          
        # Returns an error indicator 
        result = s.connect_ex((target,port)) 
        if result == 0:
            # If the port is open

            print('[{green}!{defcol}] Port {yellow}{port}{defcol} : {green}open{defcol}'.format(port = port, green = green, yellow = yellow, defcol = defcol))
            openPorts.append(port)
        else:
            # If the port is not open (i.e., closed)

            print('[{red}!{defcol}] Port {yellow}{port}{defcol} : {red}closed{defcol}'.format(port = port, red = red, yellow = yellow, defcol = defcol))
        s.close()

    # Finally displaying the total open ports on the target server
    if len(openPorts) == 0:
        # If there are 0 open ports on the target server

        print('\n[ Number of open ports found on target server : {}{}{} ]'.format(yellow, len(openPorts), defcol))
    else:
        # If there are more than 0 open ports on the target server

        print('\n[ Number of open ports found on target server : {}{}{} ]'.format(yellow, len(openPorts), defcol))
except KeyboardInterrupt:
    # If the user presses CTRL+C key combo, then we exit the script

    print('\n[ {red}Exiting Program{defcol} ]'.format(red = red, defcol = defcol)) 
    exit() 
except socket.gaierror:
    # If the hostname resolving error is encountered, then we display the error message on the console screen

    print(red_rev + '\n[ Error : Hostname could not be resolved ]' + defcol) 
    exit() 
except socket.error: 
    # If there are any other socket connections error encountered, then we display the error message on the console screen

    print(red_rev + '\n[ Error : Server not responding ]' + defcol)
    exit() 
