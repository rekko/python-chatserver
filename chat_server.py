import socket
import random
from gevent.server import StreamServer

port = 10000 + random.randrange(40000)
print('port ' + str(port))

users = []
nick = {}

def get_nick(ca):
    if ca in nick:
        return nick[ca]
    else:
        nick[ca] = 'guest' + str(ca[1])      # default nick (port)
        return nick[ca]

def chat(line, sender_ca):
    message = ""
    sender = get_nick(sender_ca)
    
    print(str(sender_ca) + sender + "> " + line)
    
    if line.find('/') == 0 and len(line.split(' ')) > 1:
        list = line.split(' ')
        command = list[0]
        arg = list[1]
        if command == '/dice':
            dice = random.randrange(int(arg))
            message = sender + " roll dice : " + dice
        elif command == '/nick':
            nick[sender_ca] = arg
            message = sender + " change nick -> " + nick[sender_ca]
            message = process_command(line, sender)
        else:
            message = sender + "> " + line
    else:
        message = sender + "> " + line
    
    broadcast(message)

def broadcast(message):
    for u in users:
        print(message, file=u, flush=True)
        
def handler(cs, ca):
    print(ca)
    f = cs.makefile('rw')
    users.append(f)
    print('welcome', file=f, flush=True)
    try:
        while True:
            line= f.readline().strip()
            chat(line, ca)

    finally:
        print('user ' + str(ca) + ' out')
        users.remove(f)

server = StreamServer(('0.0.0.0', port),
              handler)
server.serve_forever()
