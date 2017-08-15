import socket
import sys
import select

print('port? ')
port = int(input())
s = socket.socket()
s.connect(('localhost', port))
f = s.makefile('rw')
while True:
    socket_list = [sys.stdin, s]

    read_sockets, write_sockets, error_sockets = select.select(socket_list,
                                                               [],
                                                               [])

    for sock in read_sockets:
        if sock == s:
            print(f.readline())
        else:
            print(input(), file=f, flush=True)
