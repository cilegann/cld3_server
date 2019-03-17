
import socket
import time
class cld3():
    def __init__(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def establishConn(self,ip,port):
        server=(ip,port)
        print("Connected to "+ip)
        self.__sock.connect(server)
        self.__sock.settimeout(None)

    def getLang(self,t):
        self.__sock.send(t.encode(encoding='utf-8'))
        result=self.__sock.recv(1024).decode()
        while result=="X":
            self.__sock.send(t.encode(encoding='utf-8'))
            result=self.__sock.recv(1024).decode()
        return result

    def closeConn(self):
        self.__sock.close()