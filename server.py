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

            # get client's pubkey and n
            keys = tuple(map(int, c.recv(1024).decode().split()))

            self.broadcast(f'new person has joined: {username}')
            self.username_lookup[c] = username, *keys
            self.clients.append(c)

            # send public key to the client
            c.send(" ".join(map(str, self.keys[:-1])).encode())

            new_message = "Welcome to the server! Have a great time. /quit to quit"

            message_hash = hexlify(sha3_512(new_message.encode()).digest()).decode()

            new_message = crypto.encrypt(new_message, *self.username_lookup[c][1:])
            new_message = " ".join(map(str, new_message))
            new_message = message_hash + " " + new_message

            c.send(new_message.encode())

            threading.Thread(target=self.handle_client, args=(c, addr)).start()

    def broadcast(self, message: str):
        message = "server: " + message

        message_hash = hexlify(sha3_512(message.encode()).digest()).decode()
        # print(f"message: {message}, hash: {message_hash}")

        for client in self.clients:
            new_message = crypto.encrypt(message, *self.username_lookup[client][1:])
            new_message = " ".join(map(str, new_message))

            new_message = message_hash + " " + new_message
            client.send(new_message.encode())

    def handle_client(self, c: socket, addr):
        while True:
            message = c.recv(1024).decode()

            # extract hash and content
            message_hash = message.split()[0]
            message = list(map(int, message.split()[1:]))

            message = crypto.decrypt(message, self.keys[0], self.keys[2])

            if message == "/quit":
                print(f"{self.username_lookup[c][0]} has quit")
                self.clients.remove(c)
                self.broadcast(f"{self.username_lookup[c][0]} has quit")
                self.username_lookup.pop(c)
                break

            assert message_hash == hexlify(sha3_512(message.encode()).digest()).decode(),\
                "message integrity is compromised"

            print(f"{self.username_lookup[c][0]}: {message}")

            for client in self.clients:
                if client != c:
                    # add username to the message
                    new_message = self.username_lookup[c][0] + ": " + message

                    # rehash message because it was modified
                    message_hash = hexlify(sha3_512(new_message.encode()).digest()).decode()

                    new_message = crypto.encrypt(new_message, *self.username_lookup[client][1:])
                    new_message = " ".join(map(str, new_message))
                    new_message = message_hash + " " + new_message

                    client.send(new_message.encode())


if __name__ == "__main__":
    s = Server(9001)
    s.start()
