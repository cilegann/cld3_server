# from remoteCld3 import establishConn,getLang,closeConn

# s=establishConn("140.112.26.127",8886)

# texts=["hello how are you","I am fine","fuck you","You are my flower"]
# for t in texts:
#     print(getLang(s,t))

# closeConn(s)

import remoteCld3
import time
cld=remoteCld3.cld3()
cld.establishConn("140.112.26.127",8886)
for i in range(10000):
    print(cld.getLang("How are you"))
cld.closeConn()