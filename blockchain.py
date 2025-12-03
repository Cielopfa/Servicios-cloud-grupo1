import hashlib
import json
import time
from uuid import uuid4
from urllib.parse import urlparse
import requests
from flask import Flask, jsonify, request


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        self.difficulty = 4  # number of leading zeros required

        # Create the genesis block
        self.new_block(proof=100, previous_hash='1')

    def register_node(self, address):
        parsed = urlparse(address)
        if parsed.netloc:
            self.nodes.add(parsed.scheme + '://' + parsed.netloc)
        elif parsed.path:
            # when no scheme is provided
            self.nodes.add('http://' + parsed.path)

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], block['previous_hash']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbours:
            try:
                resp = requests.get(f"{node}/cadena", timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    length = data.get('longitud')
                    chain = data.get('cadena')

                    if length > max_length and self.valid_chain(chain):
                        max_length = length
                        new_chain = chain
            except requests.RequestException:
                continue

        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash=None):
        block = {
            'indice': len(self.chain) + 1,
            'timestamp': time.time(),
            'transacciones': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'emisor': sender,
            'receptor': recipient,
            'cantidad': amount,
        })
        return self.last_block['indice'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof, last_hash):
        proof = 0
        while not self.valid_proof(last_proof, proof, last_hash):
            proof += 1
        return proof

    def valid_proof(self, last_proof, proof, last_hash):
        guess = f"{last_proof}{proof}{last_hash}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:self.difficulty] == "0" * self.difficulty


# Flask app
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'mensaje': 'Blockchain Educativo - Nodo Activo',
        'nodo_id': node_identifier,
        'bloques': len(blockchain.chain),
        'endpoints': ['/cadena', '/minar', '/transacciones/nueva', '/nodos/registrar', '/nodos/resolver']
    })


@app.route('/cadena', methods=['GET'])
def full_chain():
    return jsonify({
        'cadena': blockchain.chain,
        'longitud': len(blockchain.chain)
    })


@app.route('/minar', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    last_hash = blockchain.hash(last_block)

    proof = blockchain.proof_of_work(last_proof, last_hash)

    # Reward for mining
    blockchain.new_transaction(sender="0", recipient=node_identifier, amount=1)

    block = blockchain.new_block(proof, previous_hash=last_hash)

    response = {
        'mensaje': 'Nuevo bloque minado',
        'indice': block['indice'],
        'transacciones': block['transacciones'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200


@app.route('/transacciones/nueva', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['emisor', 'receptor', 'cantidad']
    if not values or not all(k in values for k in required):
        return 'Faltan valores', 400

    index = blockchain.new_transaction(values['emisor'], values['receptor'], values['cantidad'])
    return jsonify({'mensaje': f'Transacción será añadida al bloque {index}'}), 201


@app.route('/nodos/registrar', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodos')
    if nodes is None:
        return "Error: lista de nodos vacía", 400

    for node in nodes:
        blockchain.register_node(node)

    return jsonify({'mensaje': 'Nuevos nodos registrados', 'nodos_totales': list(blockchain.nodes)}), 201


@app.route('/nodos/resolver', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        return jsonify({'mensaje': 'Cadena reemplazada', 'nueva_cadena': blockchain.chain}), 200
    else:
        return jsonify({'mensaje': 'Cadena autoritativa', 'cadena': blockchain.chain}), 200


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()

    app.run(host='0.0.0.0', port=args.port)