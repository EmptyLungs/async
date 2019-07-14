import socket
from select import select


server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_sock.bind(('localhost', 5200))
server_sock.listen(5)

monitor_sockets = []


def accept_conn(sock):
    client, addr = sock.accept()
    print('Connection from ', addr)
    monitor_sockets.append(client)


def send_message(client_sock):
    request = client_sock.recv(4096)

    if request:
        response = 'Hello world\n'.encode()
        client_sock.send(response)
    else:
        monitor_sockets.remove(client_sock)
        client_sock.close()


def event_loop():
    while True:
        ready_to_read, _, _ = select(monitor_sockets, [], [])
        for sock in ready_to_read:
            if sock is server_sock:
                accept_conn(sock)
            else:
                send_message(sock)


if __name__ == '__main__':
    monitor_sockets.append(server_sock)
    event_loop()
