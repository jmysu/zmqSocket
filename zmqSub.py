#!/usr/bin/python
import sys
import zmq

port = "23456"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)
    
if len(sys.argv) > 2:
    port1 =  sys.argv[2]
    int(port1)

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print ("Subscribe...")
#socket.connect ("tcp://localhost:%s" % port)
socket.bind ("tcp://*:%s" % port)

if len(sys.argv) > 2:
    socket.connect ("tcp://localhost:%s" % port1)

socket.setsockopt(zmq.SUBSCRIBE, b'')
while True:
    string = socket.recv()
    print string
 
