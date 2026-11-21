import socket,sys
HOSTS=["196.188.40.144","196.188.40.145","196.188.40.146","196.188.40.147","196.188.40.148","196.188.40.149","196.188.40.150","196.188.40.151","196.188.95.105","196.188.95.108","196.188.127.250"]
def m3ua(asp=1234): return bytes([1,0,0,0,0,1,0,16,0,1,0,8])+asp.to_bytes(4,"big")
def m2pa(): return bytes([1,0,0,0,11,5,0,12])+(1).to_bytes(4,"big")
for h in HOSTS:
    for port,msg,name in ((2905,m3ua(),"M3UA-ASPUP"),(3565,m2pa(),"M2PA-LS"),(3868,None,"DIAM")):
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.IPPROTO_SCTP); s.settimeout(8)
            s.connect((h,port))
            if msg: s.sendall(msg)
            try:
                d=s.recv(300)
                print(f"{h}:{port} {name} -> {'EMPTY' if not d else d[:60].hex()}")
            except socket.timeout: print(f"{h}:{port} {name} -> CONNECT-OK/silent")
            s.close()
        except Exception as e: print(f"{h}:{port} {name} -> {type(e).__name__}:{e}")
