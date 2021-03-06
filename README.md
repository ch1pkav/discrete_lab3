# Encryption | RSA algorithm
This project contains the realization of RSA algorithm to exchange messages using secure channels.

## More about modules
There are three main modules in this project:
1. [crypto.py](https://github.com/ch1pkav/discrete_lab3/blob/main/crypto.py) - module of functions to generate keys, encrypt, and decrypt a message:
   * *generate(bit_len: int)*: takes one integer - bit length of a number, generates two random prime numbers of that length using randprime function from sympy module, returns a tuple of **n, e, d** (first part of public key, second part of public key, private key)
  
   * *encrypt(message: str, n: int, pubkey: int)* - takes 3 arguments: message to encrypt, and two parts of public key; then converts characters to int numbers, divides the message into blocks (number of blocks is calculated using function *find_block_length*), encrypts each block and returns a list of encrypted blocks.
   
   * *decrypt(message: list, n: int, key: int)* - takes 3 arguments: message to decrypt(as a list of encrypted blocks), the first part of public key and private key; then decrypts each block, converts integers to characters and returns the message as a string.

Output example:
<img src = 'examples/crypto.png'>

2. [server.py](https://github.com/ch1pkav/discrete_lab3/blob/main/server.py) - module for running a server
3. [client.py](https://github.com/ch1pkav/discrete_lab3/blob/main/client.py) - module for adding clients 

## Usage instructions
1. Launch a server
```bash
python3 server.py
```
2. Open a new terminal, launch a client and enter a username
```bash
python3 client.py
```
3. Repeat the previous step to add more clients
4. Now you can start chatting using clients' terminals

## Usage example

<img src = 'examples/chat.png'>

