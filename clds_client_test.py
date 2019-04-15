import remoteCld3
import time
cld=remoteCld3.cld3()
cld.establishConn("your.ip.addr.here",portHere)
for i in range(10000):
    print(cld.getLang("How are you"))
cld.closeConn()
