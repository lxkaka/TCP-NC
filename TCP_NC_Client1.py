#-*- coding: UTF-8 -*- 
# when server ready, client can  connect to the server and send the request to server,
#then download the file according with user's command. Through decode obtain the
# source file

import socket
import time
import sys
import kodo

ip = '192.168.1.151'                                  # server's address
port = 6000
Addr = (ip , port)
sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)   # create a socket with TCP connection
def confirm(sock , client_command):                          # confirm the request from client
    sock.send(client_command)
    data = sock.recv(4096000)
    print(data)
    if data == 'Request accepted' :
        return True
    
    
try :
    '''# Set the number of symbols (i.e. the generation size in RLNC
    # terminology) and the size of a symbol in bytes
    symbols = 130
    symbol_size = 10000

    # In the following we will make an decoder factory.
    # The factories are used to build actual decoder
    decoder_factory = kodo.FullVectorDecoderFactoryBinary(
        max_symbols=symbols,
        max_symbol_size=symbol_size)

    decoder = decoder_factory.build()  '''
 
    sock.connect(Addr)
    print ('Server ready, please input command')
    EndSign = 'Start'
    while True :
	if EndSign == 'END':
	    break
        client_command = raw_input( )                                  # accept the user's  input
        if not client_command :
            continue
        
        action , filename = client_command.split( )                   # get the file name 
        if action == 'get' :
            if confirm(sock, client_command) :
                print ('Server accepted request')
                print('Receive packet and decode...')
		#f = open(filename , 'wb')
		times=0
		while True :
		    # Set the number of symbols (i.e. the generation size in RLNC
    		    # terminology) and the size of a symbol in bytes
                    symbols = 110
    		    symbol_size = 10000

   		    # In the following we will make an decoder factory.
    		    # The factories are used to build actual decoder
    		    decoder_factory = kodo.FullVectorDecoderFactoryBinary(
         	        max_symbols=symbols,
        	    	max_symbol_size=symbol_size)

    		    decoder = decoder_factory.build()
		    
		    #time.sleep(1)
                    #count=0
		    while not decoder.is_complete() :
			#count+=1
			#print(count)
		        sock.sendall('Decode not finished')
                        packet = sock.recv(40960000)
                        decoder.read_payload(packet)                      #decoding packet
		        print('packet{}/{}decoded'.format(decoder.rank(),decoder.symbols()))
		        f = open(filename ,'a')
                        f.write(decoder.copy_symbols())                   # store the decoded data
		    	f.close()
		    sock.sendall('Decode finished')
		    times+=1
		    print('Decode finished',times)
		    if times==3:
			print ('Receive file successfully!')
			break
			
		    
		    '''time.sleep(3)
		    eof = sock.recv(409600)
		    #print(eof)
		    if eof=='EOF':
		    	print ('Receive file successfully!')
			EndSign = 'END' 
	      	        break  '''
		

		#time.sleep(1) 
		
                #f.close()
            else :
        #print(confirm(sock,client_command))
                print('Server get error')
        #sock.close()
        else :
            print('Command error')
except socket.error , e :                                             #  exception handling
    print ('Error occur' , e)
finally:
    sock.close( )
    
