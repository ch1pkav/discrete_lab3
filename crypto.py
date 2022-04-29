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


def generate(a, b):
    p = randprime(a, b)
    q = randprime(a, b)
    while p == q:
        q = randprime(a, b)

    print(p, q)
    n = p * q
    print(n)
    e = 3
    print(e)
    while gcd(e, (p-1) * (q-1)) != 1:
        e += 2

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


def find_row_length(n):
    row = 34
    i = 0
    while row < n:
        row *= 100
        row += 34
        i += 1
    row //= 100
    print(row)
    return i


def encrypt(message, n, pubkey):
    message = [alphabet.find(c) + 1 for c in message]
    i = find_row_length(n)
    print(message)
    print(i)
    message = [message[j:j+i] for j in range(0, len(message), i)]
    while len(message[-1]) < i:
        message[-1].append(34)
    print(message)
    message = [sum(number * 100**index for index, number in
                   enumerate(block[::-1])) for block in message]
    print(message)
    message = [pow(block, pubkey, n) for block in message]
    print(message)
    return message


def decrypt(message, n, key):
    message = [pow(block, key, n) for block in message]
    print(message)
    decoded_message = []
    for block in message:
        buffer = []
        while block > 0:
            number = block % 100
            block //= 100
            buffer.append(number)
        print(buffer)
        decoded_message += buffer[::-1]
    print(decoded_message)
    return "".join(alphabet[i-1] if i != 34 else "" for i in decoded_message)


if __name__ == "__main__":
    keys = generate(100, 10000)
    print(keys)
    secret = encrypt("дискретнаматематика", *keys[:-1])
    print(decrypt(secret, keys[0], keys[2]))
