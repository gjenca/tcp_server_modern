#!/usr/bin/env python3
import socket
import time

socks = []
for i in range(200):
    print('socket no.',i)
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(("127.0.0.1",9999))
    socks.append((sock,sock.makefile('rw',encoding='utf-8')))
    #time.sleep(0.001)

for sock,f in socks:
    f.write('ping\n')
    f.flush()
    f.readline()

for sock,f in socks:
    f.close()
    sock.close() 
