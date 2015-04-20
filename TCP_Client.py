#-*- coding: UTF-8 -*- 
# client connect to the server and download the file according with user's command
import socket
import time
import sys

ip = '192.168.1.151'
port = 6000
Addr = (ip , port)
sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
def confirm(sock , client_command):
    sock.send(client_command)
    data = sock.recv(4096000)
    print(data)
    if data == 'Request accepted' :
	print(data)
        return True
    
try :
    sock.connect(Addr)
    print ('Server ready, please input command')
    while True :
        client_command = raw_input( )Ethernet (eth1)
        if not client_command :
            continue
        
        action , filename = client_command.split( )
        if action == 'get' :
            if confirm(sock, client_command) :
            	print ('Server accepted request')
            	f = open(filename , 'wb')
            	while True :
                    data = sock.recv(4096000)
                    if data == 'EOF' :
                    	print ('Receive file successfully!')
                        break
                    f.write(data)
                f.close()
            else :
		print(confirm(sock,client_command))
                print('Server get error')
		#sock.close()
        else :
            print('Command error')
except socket.error , e :
    print ('Error occur' , e)
finally:
    sock.close( )
    
