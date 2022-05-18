import socket, paramiko, threading, sys 
if len(sys.argv) != 3: 
    print("usage SSHServer.py <interface> <port>") 
    exit() 
class Server (paramiko.ServerInterface): 
   def check_channel_request(self, kind, chanid): 
       if kind == 'session': 
           return paramiko.OPEN_SUCCEEDED 
       return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED 
   def check_auth_password(self, username, password): 
       if (username == 'adastra') and (password == 'adastra'): 
           return paramiko.AUTH_SUCCESSFUL 
       return paramiko.AUTH_FAILED 
 
try: 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    sock.bind((sys.argv[1], int(sys.argv[2]))) 
    sock.listen(100) 
    print('[+] Escucha ...') 
    client, addr = sock.accept() 
    print("Conexión entrante")
    t = paramiko.Transport(client) 
    t.load_server_moduli() 
    server_key = paramiko.RSAKey(filename='/home/adastra/.ssh/id_rsa',password='password') 
    t.add_server_key(server_key) 
    server = Server() 
    t.start_server(server=server) 
    chan = t.accept(20) 
    print((chan.recv(1024))) 
    chan.send('SSH Connection Established!') 
    while True: 
        command= input(">: ").strip('n') 
        if command.lower() == 'exit': 
            print("Cerrando conexión...") 
            chan.send('exit') 
            break 
        chan.send(command) 
        print((chan.recv(1024)))
except Exception as e: 
    print(('[-] Excepción: ' + str(e))) 
    try: 
        t.close() 
    except: 
        pass 
