#!/usr/bin/env python3
import socket
import time
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("host",default='localhost',help='host',nargs='?')
parser.add_argument("port",default=9999,type=int,help='port',nargs='?')
args=parser.parse_args()

socks = []
for i in range(200):
    print('socket no.',i)
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('about to connect',i)
    sock.connect((args.host,args.port))
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
