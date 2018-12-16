import json

from crypto import PublicKey, hash, check_sign


class Transaction(object):
    def __init__(self, from_addr, to_addr, amount, sign, public_key: PublicKey):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.amount = amount
        self.sign = sign
        self.public_key = public_key

    def message(self):
        return "{};{};{}".format(self.from_addr, self.to_addr, self.amount)

    def validate(self):
        ok = hash(str(self.public_key)) == self.from_addr
        return ok and check_sign(self.message(), self.sign, self.public_key)

    def to_dict(self):
        return {
            'from': self.from_addr,
            'to': self.to_addr,
            'amount': self.amount,
            'sign': self.sign,
            'public_key': str(self.public_key)
        }

    def dumps(self):
        return json.dumps(self.to_dict())
    