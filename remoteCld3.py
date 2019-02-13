import socket
class cld3():
    def __init__(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def establishConn(self,ip,port):
        server=(ip,port)
        print("Connected to "+ip)
        self.__sock.connect(server)

    def getLang(self,t):
        self.__sock.send(str.encode(t))
        result=self.__sock.recv(1024).decode()
        return result

    def closeConn(self):
        self.__sock.close()