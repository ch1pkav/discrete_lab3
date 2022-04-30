from sympy import randprime


def gcd(a: int, b: int):
    """
    Returns greatest common divisor (GCD)
    """
    while b != 0:
        temp = a
        a = b
        b = temp % b
    return a


def extended_euclidean(a: int, b: int):
    """
    Find the modular multiplicative inverse of a modulo b
    """
    x = a
    y = b
    s2 = 1
    s1 = 0
    t2 = 0
    t1 = 1
    while y != 0:
        q = x // y
        r = x % y
        x = y
        y = r
        s = s2 - q * s1
        t = t2 - q * t1
        s2 = s1
        t2 = t1
        s1 = s
        t1 = t

    if (s2 < 0):
        s2 += b
    return s2


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

    d = extended_euclidean(e, (p-1) * (q-1))

    return n, e, d


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
    message = "0"
    secret = encrypt(message, *keys[:-1])
    print(secret)
    print(decrypt(secret, keys[0], keys[2]))
