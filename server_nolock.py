#!/usr/bin/env python
import socket
import multiprocessing
import logging

# nastavíme úroveň protokolovania (logging)
logging.basicConfig(level=logging.INFO)

# toto je funkcia, ktorá beží v osobitnom procese
def handle_client(client_socket, addr):

    logging.info(f'handle_client {addr} začiatok')
    sf = client_socket.makefile(mode='rw', encoding='utf-8')
    while True:
        # prečítame jeden riadok
        line = sf.readline()
        if not line:
            # klient zavrel spojenie
            break
        line = line.rstrip()
        # prečítame, čo je v tomto okamihu v súbore data.txt
        with open('data.txt', 'r') as f:
            previous = f.readline().strip()
        # zapíšeme doň to, čo nám poslal klient cez socket
        with open('data.txt', 'w') as f:
            f.write(f'{line}\n')
        # to, čo bolo v súbore predtým, pošleme klientovi cez socket s prefixom BUM:
        sf.write(f'BUM:{previous}\n')
        sf.flush()
    logging.info(f'handle_client {addr} koniec')
    # keď táto funkcia skončí, proces skončil
    # (v skutočnosti zostane bežať, Python ho znovu použije transparentne)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # aby sme mohli ihneď reštartovať server
s.bind(('', 9999))
s.listen(5)
# Vytvoríme zdieľaný zdroj: súbor data.txt
# Všetky procesy, ktoré vytvoríme, budú doň čítať a zapisovať
with open('data.txt', 'w') as f:
    f.write('INIT\n')

while True:
    cs, addr = s.accept()  # prijmeme spojenie, vytvoríme proces
    process = multiprocessing.Process(target=handle_client, args=(cs, addr))
    process.daemon = True  # tento proces pobeží "na pozadí"
    process.start()
