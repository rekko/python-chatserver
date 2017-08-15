import socket
s = socket.socket()
s.connect(('localhost', 10001))
f = s.makefile('rw')
while True:
    print(input(), file=f)
    f.flush()
    print(f.readline())
    
