#  David Beazley report
import socket
from select import select

READ = 'read'
WRITE = 'write'
tasks = []
to_read = {}
to_write = {}


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5001))
    server_socket.listen()
    print('Run server')

    while True:
        yield (READ, server_socket)
        print('Before .accept()')
        client_socket, addr = server_socket.accept()

        print('Connection from, ', addr)
        tasks.append(client(client_socket))


def client(client_socket):
    while True:
        yield ('read', client_socket)
        request = client_socket.recv(4096)

        if not request:
            break
        else:
            response = 'Hello World\n'.encode()

            yield (WRITE, client_socket)
            client_socket.send(response)

    print('Outside inner while loop')
    client_socket.close()


def event_loop():
    while any([tasks, to_read, to_write]):
        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            task = tasks.pop(0)

            reason, sock = next(task)

            if reason == READ:
                to_read[sock] = task
            if reason == WRITE:
                to_write[sock] = task
        except StopIteration:
            print('Done!')


tasks.append(server())
event_loop()
