from math import sqrt, ceil, gcd
from sympy import randprime

alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"


def eratosthenes(num):
    numbers = list(range(2, num+1))
    for i in range(2, ceil(sqrt(num))):
        for index, item in enumerate(numbers):
            if not item % i:
                numbers.pop(index)
    return numbers


def generate(bit_len):
    b = 2**bit_len - 1
    a = 2**(bit_len - 1)
    p = randprime(a, b)
    q = randprime(a, b)
    while p == q:
        q = randprime(a, b)

    # print(p, q)
    n = p * q
    # print(n)
    e = round((p+q)/8)*2+1
    # e = 3
    while gcd(e, (p-1) * (q-1)) != 1:
        e += 2
    # print(e)

    d = modInverse(e, (p-1) * (q-1))

    return n, e, d


def modInverse(a, m):
    m0 = m
    y = 0
    x = 1

    if (m == 1):
        return 0

    while (a > 1):

        # q is quotient
        q = a // m

        t = m

        # m is remainder now, process
        # same as Euclid's algo
        m = a % m
        a = t
        t = y

        # Update x and y
        y = x - q * y
        x = t

    # Make x positive
    if (x < 0):
        x = x + m0

    return x


def find_block_length(n, alphalen):
    row = alphalen
    i = 0
    while row < n:
        # print(row)
        row *= 10**(len(str(alphalen))+1)
        row += alphalen
        i += 1
    row //= 10*(len(str(alphalen))+1)
    return i


def encrypt(message, n, pubkey):
    message = [ord(c) for c in message]
    i = find_block_length(n, 257)
    # print(message)
    # print(i)
    message = [message[j:j+i] for j in range(0, len(message), i)]
    while len(message[-1]) < i:
        message[-1].append(257)
    # print(message)
    message = [sum(number * 1000**index for index, number in
                   enumerate(block[::-1])) for block in message]
    # print(message)
    message = [pow(block, pubkey, n) for block in message]
    # print(message)
    return message


def decrypt(message, n, key):
    message = [pow(block, key, n) for block in message]
    # print(message)
    decoded_message = []
    for block in message:
        buffer = []
        while block > 0:
            number = block % 1000
            block //= 1000
            buffer.append(number)
        # print(buffer)
        decoded_message += buffer[::-1]
    # print(decoded_message)
    return "".join(chr(i) if i != 257 else "" for i in decoded_message)


if __name__ == "__main__":
    keys = generate(1024)
    # keys = generate(500, 1000)
    print(keys)
    message = "lol pryit:)"
    secret = encrypt(message, *keys[:-1])
    print(secret)
    print(decrypt(secret, keys[0], keys[2]))
