#! /usr/bin/env python3
import sys, uuid
sys.path.append("../lib")       # for params

import os, socket, params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

while True:
    sock, addr = lsock.accept()

    from framedSock import framedSend, framedReceive

    if not os.fork():
        print("new child process handling connection from", addr)
        while True:
            payload = framedReceive(sock, debug)
            if not payload:
                if debug: print("child exiting")
                sys.exit(0)
            else:
                payload = payload.split(b':')
                print(payload[0])
                print(payload[1])                
                if payload[0] == b'put':
                    with open(str(uuid.uuid4()) + payload[1].decode("utf-8"), "wb") as w_file:
                        print("Opening file")
                        w_file.write(payload[2])
                        print("done w to f")
                elif payload[0] == b'get':
                    with open(payload[1], 'rb') as file_contents:
                        print(file_contents.read())
                if debug: print("rec'd: ", payload)


