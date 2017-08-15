import socket
import gevent
import gevent.threadpool

print('port? ')
port = int(input())

s = socket.socket()
s.connect(('localhost', port))
f = s.makefile('rw')

def read_message():
    while True:
        print(f.readline())

def write_message():
    while True:
        print(input(), file=f, flush=True)

pool = gevent.threadpool.ThreadPool(5)

pool.spawn(read_message)
pool.spawn(write_message)

gevent.wait()
