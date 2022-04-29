from math import sqrt, ceil, gcd
from sympy import randprime


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

    n = p * q
    e = 3
    while gcd(e, (p-1) * (q-1)) != 1:
        e += 2

    d = modInverse(e, (p-1) * (q-1))

    return e, d


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


if __name__ == "__main__":
    # print(eratosthenes(10000))
    print(generate(1000000, 100000000))
