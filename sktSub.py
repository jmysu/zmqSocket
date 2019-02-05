#!/usr/bin/python
import socket
#--------------------------------------------------------------------------------
# Cast bytes to bytearray     0   1   2   3   4   5   6   7   8   9   
zGreetingSig = bytearray(b'\xFF\x00\x00\x00\x00\x00\x00\x00\x01\x7F')
zGreetingVerMajor= bytearray(b'\x03')    
zGreetingVerMinor= bytearray(b'\x00')    
zGreetingMech= bytearray("NULL")
zGreetingEnd = bytearray(48) 
#                                        R   E   A   D   Y       S
zHandshake1  = bytearray(b'\x04\x19\x05\x52\x45\x41\x44\x59\x0B\x53')
#                            o   c   k   e   t   -   T   y   p   e     
zHandshake2  = bytearray(b'\x6F\x63\x6B\x65\x74\x2D\x54\x79\x70\x65\x00\x00\x00')
#                                S   U   B
zHandshake3  = bytearray(b'\x03\x53\x55\x42')
#
zSubStart = bytearray(b'\x00\x01\x01')
#---------------------------------------------------------------------------------
# create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# retrieve local hostname
local_hostname = socket.gethostname()
# get fully qualified hostname
local_fqdn = socket.getfqdn()
# get the according IP address
ip_address = socket.gethostbyname(local_hostname)
####
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
ip_address = s.getsockname()[0]


# output hostname, domain name and IP address
print ("working on %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))
# bind the socket to the port 23456
server_address = (ip_address, 23456)   
print ('starting up on %s port %s' % server_address)  
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)

# listen for incoming connections (server mode) with one connection at a time
sock.listen(1)
 
while True:  
    # wait for a connection
    print ('wait a connection')
    connection, client_address = sock.accept()
    try:
        print ('connection from', client_address)
        # receive the data in small chunks and print it
        while True:
            data = connection.recv(16)          
            if (data.startswith(zGreetingSig)) : #Found zmq Greeting
                print("ZMQ Greeting!")
                connection.send(zGreetingSig+zGreetingVerMajor)
            if ("NULL" in data) : #Found zmq NULL Mechnism
                print("ZMQ Ver/Mech")   
                connection.send(zGreetingVerMinor+zGreetingMech+zGreetingEnd)              
                connection.send(zHandshake1+zHandshake2+zHandshake3)
            if ("READY" in data): #Found zmq READY, Send Subscription Start
                print("ZMQ READY Subscribe")  
                connection.send(zSubStart)

            if data:
                hexdata = msg = ""
                for c in data:
                    hexdata += ("|"+c.encode('hex').upper())
                    dummy=""     
                    if (len(hexdata)< 16*3):
                        dummy = bytearray(" "*((16*3)-len(hexdata))) 
                    if 20 < ord(c) < 128:
                        msg += c
                    else:
                        msg += "."                                  
                print ("Hex: "+hexdata+"|"+dummy+"\t" + msg)
            else:
                print ("<END Connection>")
                break    

    finally:
          connection.close()