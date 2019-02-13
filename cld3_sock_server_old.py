import cld3
import socket

HOST, PORT = "0.0.0.0", 8886
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
print("CLD3 server is running at "+HOST+":"+str(PORT))

while(True):
    client, address = s.accept()
    print(str(address)+" connected")
    while(True):
        request = client.recv(1000).decode('utf-8')
        if not request: break
        print("Text in: "+request)
        result=str(cld3.get_language(request))
        print("Result: "+result)
        client.send(str.encode(result))
        print()