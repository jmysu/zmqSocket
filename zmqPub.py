#!/usr/bin/python
import zmq
import random
import sys
import time

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.PUB)
#socket.bind("tcp://*:%s" % port)
#socket.bind("tcp://127.0.0.1:5556")
socket.connect("tcp://192.168.0.15:23456")
#socket.connect("tcp://127.0.0.1:5556")
print("tcp://192.168.0.15:23456")
cnt = 999
time.sleep(3)
while True:
    #topic = random.randrange(9999,10005)
    #messagedata = random.randrange(1,215) - 80
    #print ("zmq Pub:%d %d" % (topic, messagedata))
    #socket.send("%d %d" % (topic, messagedata))
    time.sleep(1)
    socket.send("ABCDEFG-%03d" % (cnt%1000))
    cnt += 1
    time.sleep(3)
