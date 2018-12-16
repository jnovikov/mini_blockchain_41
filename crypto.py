from hashlib import sha256


class CryptoKey(object):
    def __init__(self, k, n):
        self.k = k
        self.n = n

    def dumps(self):
        return "{};{}".format(self.k, self.n)

    def __str__(self):
        return self.dumps()

    @classmethod
    def loads(cls, string):
        k, n = map(int, string.split(';'))
        return cls(k, n)


class PublicKey(CryptoKey):
    def __init__(self, e, n):
        super().__init__(e, n)

    @property
    def e(self):
        return self.k


class PrivateKey(CryptoKey):
    def __init__(self, d, n):
        super().__init__(d, n)

    @property
    def d(self):
        return self.k


def hash(x):
    return sha256(x.encode()).hexdigest()


def sign(message, key: PrivateKey):
    hashed_message = hash(message)

    return pow(int(hashed_message, 16), key.d, key.n)


def check_sign(message, signature, key: PublicKey):
    hashed_message = hash(message)
    etalon = pow(signature, key.e, key.n)
    return etalon == hashed_message
