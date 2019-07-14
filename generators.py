import socket
from select import select


tasks = []

to_read = {}
to_write = {}


def server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 5200))
    server_sock.listen(5)

    while True:
        # accept client socket
        yield server_sock, 'read'
        client, addr = server_sock.accept()
        print('Connection from ', addr)
        tasks.append(process_request(client))


def process_request(client):
    while True:
        yield client, 'read'
        request = client.recv(4096)

        # check socket data
        if not request:
            break
        else:
            response = 'Hello World\n'.encode()
            yield client, 'write'
            client.send(response)
    client.close()


def get_tasks():
    yield tasks


def event_loop():
    while any([tasks, to_read, to_write]):
        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read.keys(), to_write.keys(), [])

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            task = tasks.pop(0)
            sock, action = next(task)

            if action == 'read':
                to_read[sock] = task
            if action == 'write':
                to_write[sock] = task
        except StopIteration:
            print('Done')


if __name__ == '__main__':
    tasks.append(server())
    event_loop()
