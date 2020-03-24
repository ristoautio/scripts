import argparse
from socket import *
from threading import Thread, Semaphore

screenLock = Semaphore(value=1)
threadLimit = Semaphore(value=50)

parser = argparse.ArgumentParser(description='Scan target ports for target ip')
parser.add_argument('ip', metavar='IP', type=str, help='ip address of the target')

args = parser.parse_args()
target = args.ip


def check_port(port):
    threadLimit.acquire()
    connection = socket(AF_INET, SOCK_STREAM)
    try:
        connection.connect((target, port))
        connection.send('ping'.encode())
        result = connection.recv(100)

        screenLock.acquire()
        print(f'[+] port {port} is open')
        print(f'[+] {result}')
    except error:
        pass
    finally:
        screenLock.release()
        connection.close()
        threadLimit.release()


try:
    host = gethostbyaddr(target)
    print(f'[+] found {host[0]} @ {target}')
except:
    print('[-] host not found')
    exit(1)

for port in range(0, 9999):
    t = Thread(target=check_port, args=(port,))
    t.start()
