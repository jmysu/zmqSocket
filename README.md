# zmqSocket ZMTP sockets simulation
  ZMQ-PUB/SUB socket Python simulation, traffic dissection<br/>
  使用Python sockets模擬ZMTP-PUB/SUB的Greeting/Handshake並發送接收訂閱資料
  <br/>
  
# References
- [zmq guide](http://zguide.zeromq.org/)
- [minimum zmtp stuff](https://github.com/zeromq/zmtp/tree/master/zmtp30/C)
- [zmtp Wireshark dissector](https://github.com/whitequark/zmtp-wireshark/blob/master/zmtp-dissector.lua)

## Python sockets as subscriber <---> Pyzmq as publisher
## Python sockets as publisher <---> Pyzmq as subscriber
訂閱端 只使用 sockets (sktSub.py) <---> (zmqPub.py) 派送端 用Pyzmq 發送 <br/>
派送端 只使用 sockets (sktPub.py) <---> (zmqSub.py) 訂閱端 用Pyzmq 發送 <br/>
<br/>

### ZMQ-PUB Python Simulation
![SocketSub](pictures/sktPub.png)

### ZMQ-PUB Python Simulation Wireshark ZMTP Traffics
![SocketSub](pictures/sktPubWireshark.png)

### ZMQ-SUB Python Simulation
![SocketSub](pictures/zmqSocketSub.png)

### ZMQ-SUB Python Simulation Wireshark ZMTP Traffics
![SocketSub](pictures/zmqSocketSubWireshark.png)
