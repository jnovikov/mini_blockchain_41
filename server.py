from flask import Flask, jsonify, request
from blockchain import BlockChain, Block, Transaction

app = Flask(__name__)

genesis = Block(0, [], 0)
genesis.set_hash('0' * 64)
blockchain = BlockChain([genesis, ])
transaction_pool = []


@app.route('/')
def index():
    return jsonify(blockchain.to_dict())


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.json
    transaction = Transaction.from_dict(data)
    transaction_pool.append(transaction)
    return jsonify({"status": "OK"})


@app.route('/transactions')
def list_transactions():
    return jsonify([x.to_dict() for x in transaction_pool])


@app.route('/add_block', methods=["POST"])
def new_block():
    global transaction_pool
    data = request.json
    block = Block.from_dict(data)
    if blockchain.add_block(block):
        # Delete transactions from pool
        transaction_pool = list(filter(lambda x: x not in block.transactions, transaction_pool))
        return "New block added"
    return "Nope"


@app.route('/last_block')
def last_block():
    return jsonify(blockchain.last_block.to_dict())


if __name__ == '__main__':
    app.run(debug=True)
