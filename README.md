# Encryption | RSA algorithm
This project containes the realization of RSA algorithm to exchange messages using secure channels.

## More about modules
There are three main modules in this project:
1. [crypto.py](https://github.com/ch1pkav/discrete_lab3/blob/main/crypto.py) - module of functions to generate keys, encrypt and decrypt message:
   * *generate(bit_len: int)*: takes one integer - bit length of a number, generates two random prime numbers of that length using randprime function from sympy module, returns tuple of **n, e, d** (first part of public key, second part of public key, private key)
   * *encrypt(message: str, n: int, pubkey: int)*
   * *decrypt(message: str, n: int, key: int)*

3. [server.py](https://github.com/ch1pkav/discrete_lab3/blob/main/server.py) - module for running a server
4. [client.py](https://github.com/ch1pkav/discrete_lab3/blob/main/client.py) - module for adding clients 

## Usage instructions

## Usage example
