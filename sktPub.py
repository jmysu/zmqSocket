#!/usr/bin/python
"""
    ZMQ PUB simulation with pure Python sockets
"""
import socket
import time
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
#                                P   U   B
zHandshake3  = bytearray(b'\x03\x50\x55\x42')
#
zSubStart = bytearray(b'\x00\x01\x01')
#---------------------------------------------------------------------------------
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 23456)
print ('connecting to %s port %s' % server_address)
sock.connect(server_address)
PubStart = False
try:
    sock.send(zGreetingSig)
    print("Sending ZMQ Greeting")
    while True:
        data = sock.recv(16)
        if (data.startswith(zGreetingSig)) : #Found zmq Greeting
            print("Got ZMQ Greeting!")
            sock.send(zGreetingVerMajor+zGreetingVerMinor)
            print("ZMQ Ver/Mech")   
            sock.send(zGreetingMech+zGreetingEnd)              
            sock.send(zHandshake1+zHandshake2+zHandshake3)
        if ("READY" in data) : #Found READY   
            ba = bytearray('\x00\x06\x30\x31\x32\x33\x34\x35')
            sock.send(ba)              

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
     sock.close()