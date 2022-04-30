import socket
import crypto
import threading
from hashlib import sha3_512
from binascii import hexlify


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

    def broadcast(self, message: str):
        for client in self.clients:
            message = "server: " + message

            message_hash = hexlify(sha3_512(message.encode()).digest()).decode()

            message = crypto.encrypt(message, *self.username_lookup[client][1:])
            message = " ".join(map(str, message))

            message = message_hash + " " + message

            client.send(message.encode())

    def handle_client(self, c: socket, addr):
        while True:
            message = c.recv(1024).decode()

            message_hash = message.split()[0]
            message = list(map(int, message.split()[1:]))

            message = crypto.decrypt(message, self.keys[0], self.keys[2])

            assert message_hash == hexlify(sha3_512(message.encode()).digest()).decode(),\
                "message integrity is compromised"

            for client in self.clients:
                if client != c:
                    message = self.username_lookup[c][0] + ": " + message
                    message_hash = hexlify(sha3_512(message.encode()).digest()).decode()
                    message = crypto.encrypt(message, *self.username_lookup[client]
                                         [1:])
                    message = " ".join(map(str, message))
                    message = message_hash + " " + message

                    client.send(message.encode())


if __name__ == "__main__":
    s = Server(9001)
    s.start()
