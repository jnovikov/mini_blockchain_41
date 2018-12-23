import requests
import json
from blockchain import Transaction, Block
from crypto import PublicKey, PrivateKey, sign

b_url = 'http://localhost:5000'


def add_transaction(to, amount, addr, public: PublicKey, private: PrivateKey):
    t = Transaction(addr, to, amount, '', public)
    print(t.message())
    t.sign = sign(t.message(), private)
    data = t.to_dict()
    resp = requests.post(b_url + '/add_transaction', json=data)
    return resp.text


def get_transactions():
    resp = requests.get(b_url + '/transactions')
    return resp.json()


def get_last_block():
    last_block = requests.get(b_url + '/last_block').json()
    return last_block


def mine():
    transactions = get_transactions()
    transactions = [Transaction.from_dict(x) for x in transactions]
    last_block = get_last_block()
    block = Block(last_block['id'] + 1, transactions, 0)
    while not block.get_hash(last_block['hash']).startswith('0000'):
        block.nonce += 1
    block.set_hash(block.get_hash(last_block['hash']))
    r = requests.post(b_url + '/add_block', json=block.to_dict())
    return r.text


def get_blocks():
    blocks = requests.get(b_url + '/').json()
    blocks = [Block.from_dict(x) for x in blocks['blocks']]
    return blocks


def get_balance(addr):
    blocks = get_blocks()
    transactions = sum((x.transactions for x in blocks), [])
    amount = 0
    for transaction in transactions:
        if transaction.from_addr == addr:
            amount -= transaction.amount
        if transaction.to_addr == addr:
            amount += transaction.amount
    return amount


f = open('wallet.json', 'r')
wallet = json.loads(f.read())
f.close()

public_key = PublicKey.loads(wallet['public_key'])
private_key = PrivateKey.loads(wallet['private_key'])
address = wallet['address']

print(add_transaction('0' * 64, 1, address, public_key, private_key))
print(get_transactions())

print(mine())
print(get_transactions())

# get_blocks()
print(get_balance(address))
