import sys
import os
import socket

ip = '127.0.0.1'
port = 2222
# for i in range(255):
#     os.startfile("D:\\文档\\CTF\\buuoj\\逆向\\[FlareOn4]greek_to_me\\greek_to_me.exe")
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect((ip, port))
#     s.send(i.to_bytes(1, "big"))
#     data = s.recv(1024)
#     s.close()
#     print(data)
#     if 'Congratulations' in str(data, encoding="utf-8"):
#         print("%x" % i)
#         break


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))
s.send(0xa2.to_bytes(1, "big"))
s.close()