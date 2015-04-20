#-*- coding: UTF-8 -*- 

import SocketServer
import string
import time

class MyTcpServer(SocketServer.BaseRequestHandler):
    ''' build a TCP server , client can connect to the server and from it download  the 
    file. here use SocketServer to realize '''
    
    def handle (self):
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
                print('Starting send file...')
                f = open(filename , 'rb')
                while True :
                    data = f.read( )
                    if not data :
                        break
                   # while len(data)>0 :
                    self.request.send(data)
                f.close()
                time.sleep(1)
                self.request.send('EOF')
                print('Send file successfully!')
                break
        self.request.close()
        print('Disconnected from', self.client_address)

                                   
if __name__ == "__main__":
    print('Server waiting for connection...')
    host = ''
    port = 6000
    s = SocketServer.ThreadingTCPServer((host,port), MyTcpServer)
    s.serve_forever()

