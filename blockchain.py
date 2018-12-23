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

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['from'],
            data['to'],
            data['amount'],
            data['sign'],
            PublicKey.loads(data['public_key'])
        )

    def __eq__(self, other):
        return (self.from_addr == other.from_addr
                and self.to_addr == other.to_addr
                and self.amount == other.amount)

    def dumps(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.dumps()


class Block(object):
    def __init__(self, block_id, transactions: [Transaction], nonce):
        self.id = block_id
        self.transactions = transactions
        self.nonce = nonce
        self.hash = ''

    @property
    def transactions_hash(self):
        input = ''
        for transaction in self.transactions:
            # hash(transaction)
            input += str(transaction)
        return hash(input)

    def get_hash(self, prev_hash):
        return hash(prev_hash + self.transactions_hash + str(self.nonce))

    def set_hash(self, block_hash):
        self.hash = block_hash

    def to_dict(self):
        return {
            'id': self.id,
            'transactions': [x.to_dict() for x in self.transactions],
            'hash': self.hash,
            'transaction_hash': self.transactions_hash,
            'nonce': self.nonce
        }

    def dumps(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['id'],
            [Transaction.from_dict(x) for x in data['transactions']],
            data['nonce'],
        )


class BlockChain(object):
    def __init__(self, blocks: [Block]):
        self.blocks = blocks

    @property
    def last_block(self):
        return self.blocks[-1]

    def add_block(self, block: Block):
        new_hash = block.get_hash(self.last_block.hash)
        for transaction in block.transactions:
            pass
            # transaction.validate()
        if BlockChain.challenge(new_hash):
            block.set_hash(new_hash)
            self.blocks.append(block)
            return True
        return False

    @staticmethod
    def challenge(hash: str):
        return hash.startswith('0' * 4)

    def to_dict(self):
        return {
            'blocks': [x.to_dict() for x in self.blocks]
        }
