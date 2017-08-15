import socket
from gevent.server import StreamServer

users = []

def handler(cs, ca):
    print(ca)
    f = cs.makefile('rw')
    users.append(f)
    try:
        while True:
            line = f.readline()
            for u in users:
                print(line, file=u, flush=True)
    finally:
        users.remove(f)

server = StreamServer(('0.0.0.0', 10001),
              handler)
server.serve_forever()
