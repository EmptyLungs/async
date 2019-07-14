import socket
import selectors


selector = selectors.DefaultSelector()


def server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 5200))
    server_sock.listen(5)

    selector.register(fileobj=server_sock, events=selectors.EVENT_READ, data=accept_conn)


def accept_conn(sock):
    client, addr = sock.accept()
    selector.register(fileobj=client, events=selectors.EVENT_READ, data=send_message)


def send_message(client_sock):
    request = client_sock.recv(4096)

    if request:
        response = 'Hello world\n'.encode()
        client_sock.send(response)
    else:
        selector.unregister(client_sock)
        client_sock.close()


def event_loop():
    while True:
        events = selector.select()
        for key, _ in events:
            callback = key.data
            callback(key.fileobj)


if __name__ == '__main__':
    server()
    event_loop()
