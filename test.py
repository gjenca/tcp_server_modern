#!/usr/bin/env python3
import socket
import time
import sys

socks = []
for i in range(200):
    print('socket no.',i)
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('about to connect',i)
    sock.connect(("127.0.0.1",9999))
    print('connected',i)
    socks.append((sock,sock.makefile('rw',encoding='utf-8')))
    time.sleep(0.005)

for i,(sock,f) in enumerate(socks):
    f.write(f'ping {i}\n')
    f.flush()

for i,(sock,f) in enumerate(socks):
    sys.stdout.write(f'{i} -> {f.readline()}')
    f.close()
    sock.close() 
