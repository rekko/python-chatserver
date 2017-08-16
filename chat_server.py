import socket
import random
from gevent.server import StreamServer

port = 10000 + random.randrange(40000)
print('port ' + str(port))

users = []
nick = {}

def get_nick(ca):
    if ca in nick.keys():
        return nick[ca]
    else:
        nick[ca] = 'guest' + str(ca[1])      # default nick (port)
        return nick[ca]

def is_command(line):
    if line.find('/') == 0 and line.find(' ') > 0 and len(line.split(' ')) > 1:
        return True
    else:
        return False

def process_command(line, sender_ca):
    sender = get_nick(sender_ca)

    # check command
    list = line.split(' ')
    command = list[0]
    arg = list[1]
    
    if command == '/dice':
        dice = random.randrange(int(arg))
        message = sender + " roll dice : " + str(dice) + "/" + arg + ")"
    elif command == '/nick':
        nick[sender_ca] = arg
        message = sender + " changes nick -> " + nick[sender_ca]
    else:
        message = 'invalid command'
    
    return message

def chat(line, sender_ca):
    message = ""
    sender = get_nick(sender_ca)
    
    print(str(sender_ca) + sender + "> " + line)
    
    if is_command(line):
        message = process_command(line, sender_ca)
    else:
        message = sender + "> " + line
    
    broadcast(message)

def broadcast(message):
    for u in users:
        print(message, file=u, flush=True)

def broadcast_except(message, f):
    for u in users:
        if u == f:
            continue
        print(message, file=u, flush=True)
        
def handler(cs, ca):
    print(str(ca) + get_nick(ca) + ' in')
    f = cs.makefile('rw')
    users.append(f)

    print('welcome ' + get_nick(ca), file=f, flush=True)
    broadcast(get_nick(ca) + ' in')

    try:
        while True:
            line= f.readline().strip()
            chat(line, ca)
    except:
        print(str(ca) + get_nick(ca) + ' out')
    finally:
        broadcast_except(get_nick(ca) + ' out', f)
        users.remove(f)
        nick.pop(ca)

server = StreamServer(('0.0.0.0', port),
              handler)
server.serve_forever()
