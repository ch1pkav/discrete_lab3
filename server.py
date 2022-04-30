import socket
import crypto
import threading


class Server:

    def __init__(self, port: int) -> None:
        self.host = '127.0.0.1'
        self.port = port
        self.clients = []
        self.username_lookup = {}
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)

        # generate keys ...
        self.keys = crypto.generate(512)

        while True:
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            print(f"{username} tries to connect")

            keys = tuple(map(int, c.recv(1024).decode().split()))
            self.broadcast(f'new person has joined: {username}')
            self.username_lookup[c] = username, *keys
            self.clients.append(c)

            # send public key to the client
            c.send(" ".join(map(str, self.keys[:-1])).encode())
            threading.Thread(target=self.handle_client, args=(c,
                                                              addr,)).start()

    def broadcast(self, msg: str):
        for client in self.clients:

            msg = crypto.encrypt(msg, *self.username_lookup[client][1:])
            msg = " ".join(map(str, msg))

            client.send(msg.encode())

    def handle_client(self, c: socket, addr):
        while True:
            msg = c.recv(1024).decode()
            msg = list(map(int, msg.split()))

            msg = crypto.decrypt(msg, self.keys[0], self.keys[2])

            for client in self.clients:
                if client != c:
                    msg = self.username_lookup[c][0] + ": " + msg
                    msg = crypto.encrypt(msg, *self.username_lookup[client]
                                         [1:])
                    msg = " ".join(map(str, msg))

                    client.send(msg.encode())


if __name__ == "__main__":
    s = Server(9001)
    s.start()
