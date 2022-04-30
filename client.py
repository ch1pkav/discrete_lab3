import socket
import threading
import crypto
from hashlib import sha3_512
from binascii import hexlify


class Client:
    def __init__(self, server_ip: str, port: int, username: str) -> None:
        self.server_ip = server_ip
        self.port = port
        self.username = username

    def init_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server_ip, self.port))
        except Exception as e:
            print("[client]: could not connect to server: ", e)
            return

        self.s.send(self.username.encode())

        self.keys = crypto.generate(512)

        self.s.send(" ".join(map(str, self.keys[:-1])).encode())

        self.serverkey = list(map(int, self.s.recv(1024).decode().split()))

        message_handler = threading.Thread(target=self.read_handler, args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler, args=())
        input_handler.start()

    def read_handler(self):
        while True:
            message = self.s.recv(1024).decode()

            message_hash = message.split()[0]

            message = list(map(int, message.split()[1:]))

            message = crypto.decrypt(message, self.keys[0], self.keys[2])

            # check hash
            assert message_hash == hexlify(sha3_512(message.encode()).digest()).decode(),\
                "message integrity is compromised"

            print(message)

    def write_handler(self):
        while True:
            message = input()

            # create hash in text form
            message_hash = hexlify(sha3_512(message.encode()).digest()).decode()

            message = crypto.encrypt(message, self.serverkey[0], self.serverkey[1])

            message = " ".join(map(str, message))

            # append hash to message
            message = message_hash + " " + message
            self.s.send(message.encode())


if __name__ == "__main__":
    username = input("Enter username: ")
    cl = Client("127.0.0.1", 9001, username)
    cl.init_connection()
