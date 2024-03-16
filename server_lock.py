#!/usr/bin/env python
import socket
import multiprocessing
import logging

# nastavime uroven protokolovania (logging)
logging.basicConfig(level=logging.INFO)

# vytvorime Lock

lock=multiprocessing.Lock()

# toto je funkcia, ktora bezi v osobitnom procese
def handle_client(client_socket,addr,l):

    logging.info(f'handle_client {addr} start')
    sf=client_socket.makefile(mode='rw',encoding='utf-8')
    while True:
        # precitame jeden riadok
        line=sf.readline()
        if not line:
            # klient zavrel spojenie
            break
        line=line.rstrip()
        # zamkneme;
        # ak je l v stave "zamknute", l.acquire() blokuje
        # az do odomknutia
        l.acquire()
        # ZACIATOK KRITICKEJ SEKCIE
        # precitame, co je v tomto okamihu v subore data.txt
        with open('data.txt','r') as f:
            previous=f.readline().strip()
        # zapiseme don to, co nam poslal klient cez socket
        with open('data.txt','w') as f:
            f.write(f'{line}\n')
        # KONIEC KRITICKEJ SEKCIE
        # odomkneme
        l.release()
        # to, co bolo v subore predtym posleme klientovi cez socket s prefixom BUM:
        sf.write(f'BUM:{previous}\n')
        sf.flush()
    logging.info(f'handle_client {addr} end')
    # ked tato funkcia skonci, proces skoncil
    # (v skutocnosti zostane bezat, Python ho znovupouzije transparentne)


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # TCP socket
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) # aby sme mohli ihned restartovat server
s.bind(('',9999))
s.listen(5)
# Vytvorime zdielany zdroj: subor data.txt
# Vsetky procesy, ktore vytvorime budu don citat a zapisovat
with open('data.txt','w') as f:
    f.write('INIT\n')

while True:
    cs,addr=s.accept() # prijmeme spojenie, vytvorime proces
    process=multiprocessing.Process(target=handle_client,args=(cs,addr,lock))
    process.daemon=True # tento proces pobezi "na pozadi"
    process.start()

