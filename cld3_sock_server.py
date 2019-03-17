import socket, threading
import cld3
HOST = '0.0.0.0'
PORT = 8886 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reuse tcp
# sock.settimeout(10)
# sock.settimeout(None)
sock.bind((HOST, PORT))
sock.listen(7)
print("CLD3 server is running at "+HOST+":"+str(PORT))
#lock = threading.Lock()

class CLD3Server(threading.Thread):
    def __init__(self, socket, adr):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address= adr 

    def run(self):
        print("Connected: "+str(self.address))
        while True:
            try:
                request = self.socket.recv(4096)
                request=request.decode('utf-8')
                if not request:
                    break
                print("Text in: "+request)
                result=str(cld3.get_language(request))
                print("Result: "+result)
                client.send(str.encode(result))
                print()
                #lock.release()
            except socket.timeout as e:
                print(str(e))
                break
            except UnicodeDecodeError as e:
                print("Decode Error")
                client.send(str.encode("X"))
        self.socket.close()
        print("Disconnect")

if __name__ == "__main__":
    while True:
        (client, adr) = sock.accept()
        CLD3Server(client, adr).start()
    sock.close()

