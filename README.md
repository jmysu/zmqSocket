# zmqSocket
  ZMQ-SUB socket Python simulation<br/>
  使用Phthon sockets模擬ZMTP-SUB的Greeting/Handshake 並接收訂閱資料
  <br/>
  
# References
- [zmq guide](http://zguide.zeromq.org/)
- [minimum zmtp stuff](https://github.com/zeromq/zmtp/tree/master/zmtp30/C)
- [zmtp Wireshark dissector](https://github.com/whitequark/zmtp-wireshark/blob/master/zmtp-dissector.lua)

## Python sockets as subscriber <---> Pyzmq as publisher
訂閱端 只使用 sockets <---> 派送端 用Pyzmq 發送 
<br/>
<br/>

### ZMQ-SUB Python Simulation
![SocketSub](pictures/zmqSocketSub.png)

### ZMQ-SUB Python Simulation Wireshark ZMTP traffics
![SocketSub](pictures/zmqSocketSubWireshark.png)
