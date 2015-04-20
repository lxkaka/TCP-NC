#-*- coding: UTF-8 -*- 

import SocketServer
import string
import time
import os
import kodo


class MyTcpServer(SocketServer.BaseRequestHandler):
    ''' build a TCP server , client can connect to the server and from it download  the 
    file. here use SocketServer to realize. On this base we use RLNC to encode the data
    then deliver '''
    
    def handle (self):                                 # overwrite the 'handle' method                                    
        print 'Connected from', self.client_address
        
        while True :
            ReData = self.request.recv(40960)
            if not ReData :
                print('No Request')
                break
            else :
                action , filename = ReData.split( )        # receive the client's request and get the file name
                self.request.sendall ('Request accepted')
                
                time.sleep(1)
                ###############################   Encode part
                # Set the number of symbols(the generation size in RLNC terminology
                # Set the size of a symbol in bytes
                symbols = 20
                symbol_size = 1000
                
                # In the following we will make an encoder factory.
                #The factories are used to build actual encoder
                encoder_factory = kodo.FullVectorEncoderFactoryBinary(
                    max_symbols=symbols,
                    max_symbol_size=symbol_size)

                encoder = encoder_factory.build()
                
                # get the data to encode      
                f = open(filename , 'rb')
                #start = time.time()
                data = f.read( )
                if not data :
                    print('No valid data')  
                f.close() 
                   # Assign the data buffer to the encoder so that we can
                   # produce encoded symbols
                encoder.set_symbols(data)
                    #self.request.send(data)
                print('Encoding and starting send file...')
		packet_number = 1
                start = time.time()
                while True :
		    FiSign = self.request.recv(40960)
		    print FiSign
		    if FiSign =='Decode finished' :
			break
		    else :
                        packet = encoder.write_payload()                        # Generate an encoded packet
		        print('packet{} encoded'.format(packet_number))
			#print packet
                        self.request.send(packet)
		        packet_number+=1
                    #if not self.request.recv(40960) :
		    #if FiSign =='Decode finished' :
                    #    break
		    
                    
                time.sleep(1)
                self.request.sendall('EOF')
                print('Send coded data successfully!')  
                finish = time.time() 

                break
        self.request.close()
        DeliverTime = finish-start
        print'Disconnected from', self.client_address
        FileSize = os.path.getsize(filename)
        print('File size :',FileSize )
        print('Deliver time :', DeliverTime)
        print('Average Thoughput: {} MB/s'.format(FileSize/(DeliverTime*1000000)))

                                   
if __name__ == "__main__":
    print('Server waiting for connection...')
    host = ''
    port = 6000
    s = SocketServer.ThreadingTCPServer((host,port), MyTcpServer)
    s.allow_reuse_address = True
    s.serve_forever()

