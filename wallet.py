import json
from math import sqrt
from crypto import PublicKey, PrivateKey, hash
import random


def is_prime(x):
    for i in range(2, int(sqrt(x)) + 1):
        if x % i == 0:
            return False
    return True


def generate_prime(l, r):
    n = random.randint(l, r)
    while not is_prime(n):
        n = random.randint(l, r)
    return n


def generate_keys():
    p = generate_prime(1000, 2000)
    q = generate_prime(2000, 3000)
    assert p != q
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 101
    d = 1
    while (d * e) % phi != 1:
        d += 1
    return PublicKey(e, n), PrivateKey(d, n)


public, private = generate_keys()
wallet = {
    'public_key': public.dumps(),
    'private_key': private.dumps(),
    'address': hash(str(public))
}
o = open('wallet.json', 'w')
print(json.dumps(wallet), file=o)
o.close()
