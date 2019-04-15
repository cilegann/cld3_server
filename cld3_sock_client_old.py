import socket
import time
SERVER_IP='your.ip.addr.here'
SERVER_PORT=portHere
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server=(SERVER_IP,SERVER_PORT)
print("Connected to "+SERVER_IP)
sock.connect(server)

texts=["hello how are you","I am fine","fuck you","You are my flower"]
for t in texts:
    print(t)
    sock.send(str.encode(t))
    result=sock.recv(1024)
    print(result.decode())

sock.close()




