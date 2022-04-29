import socke

        # exchange public keys

        # receive the encrypted secret key

        message_handler = threading.Thread(target=self.read_handler, args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler, args=())
        input_handler.start()

    def read_handler(self):
        while True:
            message = self.s.recv(1024).decode()

            # decrypt message with the secrete key

            # ...

            print(message)

    def write_handler(self):
        while True:
            message = input()

            # encrypt message with the secrete key

            # ...

            self.s.send(message.encode())


if __name__ == "__main__":
    cl = Client("127.0.0.1", 9001, "b_g")
    cl.init_connection()
