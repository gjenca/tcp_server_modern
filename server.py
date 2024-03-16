#!/usr/bin/env python
import socket
import multiprocessing
import logging

logging.basicConfig(level=logging.INFO)

def handle_client(client_socket,addr):

    logging.info(f'handle_client {addr} start')
    f=client_socket.makefile(mode='rw',encoding='utf-8')
    while True:
        line=f.readline()
        if not line:
            break
        line=line.rstrip()
        f.write(f'BUM:{line}\n')
        f.flush()
    logging.info(f'handle_client {addr} end')


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # TCP socket
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) # aby sme mohli ihned restartovat server
s.bind(('',9999))
s.listen(5)


while True:
    cs,addr=s.accept()
    process=multiprocessing.Process(target=handle_client,args=(cs,addr))
    process.daemon=True
    process.start()

