import re, base64

def framedSend(sock, payload, debug=0):
     if debug: print("framedSend: sending %d byte message" % len(payload))
     msg = str(len(payload)).encode() + b':' + payload
     while len(msg):
         nsent = sock.send(msg)
         msg = msg[nsent:]


# add file name and contents of file to payload
def framedSendFile(sock, ffile, debug=0):
    payload = b'put:' + ffile.name.encode() + b':' + base64.encodestring(ffile.read())
    framedSend(sock, payload, debug)


def framedRequestFile(sock, file_name, debug=0):
    payload = b'get:' + file_name.encode()
    framedSend(sock, payload, debug)

rbuf = b""                      # static receive buffer

def framedReceive(sock, debug=0):
    global rbuf
    state = "getLength"
    msgLength = -1
    while True:
         if (state == "getLength"):
             match = re.match(b'([^:]+):(.*)', rbuf) # look for colon
             if match:
                  lengthStr, rbuf = match.groups()
                  try: 
                       msgLength = int(lengthStr)
                  except:
                       if len(rbuf):
                            print("badly formed message length:", lengthStr)
                            return None
                  state = "getPayload"
         if state == "getPayload":
             if len(rbuf) >= msgLength:
                 payload = rbuf[0:msgLength]
                 rbuf = rbuf[msgLength:]
                 return payload
         r = sock.recv(100)
         rbuf += r
         if len(r) == 0:
             if len(rbuf) != 0:
                 print("FramedReceive: incomplete message. \n  state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))
             return None
         if debug: print("FramedReceive: state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))
