import socket
import threading
import crypto


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

        # create key pairs
        self.keys = crypto.generate(512)

        # exchange public keys

        self.s.send(" ".join(map(str, self.keys[:-1])).encode())

        # receive the encrypted secret key

        self.serverkey = list(map(int, self.s.recv(1024).decode().split()))

        message_handler = threading.Thread(target=self.read_handler, args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler, args=())
        input_handler.start()

    def read_handler(self):
        while True:
            message = self.s.recv(1024).decode()

            message = map(int, message.split())
            # decrypt message with the secret key
            message = crypto.decrypt(message, self.keys[0], self.keys[2])

            print(message)

    def write_handler(self):
        while True:
            message = input()

            # encrypt message with the secrete key
            message = crypto.encrypt(message, self.serverkey[0], self.serverkey[1])

            message = " ".join(map(str, message))
            # print(message)

            # ...

            self.s.send(message.encode())


if __name__ == "__main__":
    username = input("Enter username: ")
    cl = Client("127.0.0.1", 9001, username)
    cl.init_connection()
