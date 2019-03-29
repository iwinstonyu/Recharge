import socket

# 服务端口
try:
    HttpPort = int(input('Please input the server port, default port is 9420:'))
except Exception as e:
    HttpPort = 9420

# 地址信息
HttpHost = ('localhost', HttpPort)
# 返回的头部信息
HttpResponseHeader = '''HTTP/1.1 200 OK
Content-Type: text/html

'''

HttpResponseBody = ''
# 新的socket
ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ListenSocket绑定与监听
ListenSocket.bind(HttpHost)
ListenSocket.listen(100)

# 报头与报文分隔符
LineSeparator = '\r\n\r\n'

print('The server is running on port %d' % HttpPort)
print('The url is http://localhost:%d' % HttpPort)

while True:
    HttpResponseBody = 'Hi : )'
    Client, Address = ListenSocket.accept()
    Request = Client.recv(1024).decode(encoding='utf-8')
    print("BEG RECV==============================\r\n")
    print(Request)
    print("END RECV==============================\r\n")
    Client.sendall((HttpResponseHeader + HttpResponseBody).encode(encoding='utf-8'))
    Client.close()