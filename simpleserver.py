import socket
import threading #Threading allows server to handle multiple connections at once
import sys

class Server:

    #set the socket to the socket method in socket lib
    #param1 says we use ip v4.
    #param2 says we use TCP connection, for UDP, use socket.DGRAM
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    def __init__(self):
        self.sock.bind(('0.0.0.0', 10000))
        self.sock.listen(1) #number of pending connetions to allow.
        """Sockets must be bound and listening in order to accept connections"""



    def tHandler(self, connexion, cl_addr):
            #global connections
            while True:
                data = connexion.recv(1024)
                for c in self.connections:
                    c.send(bytes(data))
                if not data:
                    #connections.remove(connexion)
                    #connexion.close()
                    break
    def run(self):
        while True:
                connexion, cl_addr = self.sock.accept() #returns connection and address
                cThread = threading.Thread(target=self.tHandler, args=(connexion,cl_addr))
                cThread.daemon = True #lets program exit even if a thread is running
                cThread.start()
                self.connections.append(connexion)
                print(self.connections)
class Client:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        def sendMsg(self):
            while True:
                self.sock.send(bytes(input("Say something nice!: "),'utf-8')) #WHERE THE FILTERING HAPPENS
        
        def __init__(self, addr):
                self.sock.connect((addr, 10000))
                #set up input threading
                iThread = threading.Thread(target=self.sendMsg)
                iThread.daemon = True
                iThread.start()
                
                while True:
                        data = self.sock.recv(1024)
                        if not data:
                            break
                        print(data)


#are we server or client?
if (len(sys.argv) > 1):
    client = Client(sys.argv[1])
else: #we are the server
    server = Server()
    server.run()
