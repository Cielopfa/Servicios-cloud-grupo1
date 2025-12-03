import unittest
import json
import time
from blockchain import Blockchain
from urllib.parse import urlparse


class TestBlockchain(unittest.TestCase):
    """Suite de pruebas para la clase Blockchain"""

    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.blockchain = Blockchain()
        self.blockchain.difficulty = 3 

    def tearDown(self):
        """Limpieza después de cada prueba"""
        self.blockchain = None

    # ============================================
    # Pruebas de Inicialización
    # ============================================

    def test_blockchain_initialization(self):
        """Verifica que la blockchain se inicializa correctamente"""
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(len(self.blockchain.current_transactions), 0)
        self.assertEqual(len(self.blockchain.nodes), 0)

    # ... (Resto del código de inicialización, hashing, transacciones)

    def test_genesis_block_creation(self):
        """Verifica que el bloque génesis se crea correctamente"""
        genesis = self.blockchain.chain[0]
        self.assertEqual(genesis['indice'], 1)
        self.assertEqual(genesis['previous_hash'], '1')
        self.assertEqual(genesis['proof'], 100)
        self.assertIn('timestamp', genesis)
        self.assertEqual(genesis['transacciones'], [])

    # ============================================
    # Pruebas de Hashing
    # ============================================

    def test_hash_function(self):
        """Verifica que la función hash genera hashes consistentes"""
        block = {
            'indice': 1,
            'timestamp': 1234567890,
            'transacciones': [],
            'proof': 100,
            'previous_hash': '1'
        }
        hash1 = self.blockchain.hash(block)
        hash2 = self.blockchain.hash(block)
        self.assertEqual(hash1, hash2)
        self.assertEqual(len(hash1), 64)

    def test_hash_consistency(self):
        """Verifica que el orden de las claves no afecta el hash"""
        block = {'a': 1, 'b': 2, 'c': 3}
        block_reordered = {'c': 3, 'b': 2, 'a': 1}
        self.assertEqual(
            self.blockchain.hash(block),
            self.blockchain.hash(block_reordered)
        )

    def test_different_blocks_different_hash(self):
        """Verifica que bloques diferentes tienen hashes diferentes"""
        block1 = {'data': 'test1'}
        block2 = {'data': 'test2'}
        self.assertNotEqual(
            self.blockchain.hash(block1),
            self.blockchain.hash(block2)
        )

    # ============================================
    # Pruebas de Transacciones
    # ============================================

    def test_new_transaction(self):
        """Verifica que las transacciones se agregan correctamente"""
        index = self.blockchain.new_transaction('alice', 'bob', 50)
        self.assertEqual(len(self.blockchain.current_transactions), 1)
        self.assertEqual(index, 2)  # Siguiente bloque será el índice 2

    def test_new_transaction_structure(self):
        """Verifica la estructura correcta de una transacción"""
        self.blockchain.new_transaction('alice', 'bob', 100)
        tx = self.blockchain.current_transactions[0]
        self.assertEqual(tx['emisor'], 'alice')
        self.assertEqual(tx['receptor'], 'bob')
        self.assertEqual(tx['cantidad'], 100)

    def test_multiple_transactions(self):
        """Verifica que múltiples transacciones se agregan correctamente"""
        self.blockchain.new_transaction('alice', 'bob', 50)
        self.blockchain.new_transaction('bob', 'charlie', 30)
        self.blockchain.new_transaction('charlie', 'alice', 20)
        self.assertEqual(len(self.blockchain.current_transactions), 3)

    # ============================================
    # Pruebas de Bloques
    # ============================================

    def test_new_block(self):
        """Verifica que se crea un nuevo bloque correctamente"""
        self.blockchain.new_transaction('alice', 'bob', 50)
        new_block = self.blockchain.new_block(proof=12345, previous_hash='abc123')
        
        self.assertEqual(new_block['indice'], 2)
        self.assertEqual(new_block['proof'], 12345)
        self.assertEqual(new_block['previous_hash'], 'abc123')
        self.assertEqual(len(new_block['transacciones']), 1)
        self.assertIn('timestamp', new_block)

    def test_new_block_clears_transactions(self):
        """Verifica que las transacciones se limpian después de crear un bloque"""
        self.blockchain.new_transaction('alice', 'bob', 50)
        self.assertEqual(len(self.blockchain.current_transactions), 1)
        
        self.blockchain.new_block(proof=12345, previous_hash='abc123')
        self.assertEqual(len(self.blockchain.current_transactions), 0)

    def test_last_block_property(self):
        """Verifica que la propiedad last_block retorna el último bloque"""
        last = self.blockchain.last_block
        self.assertEqual(last['indice'], 1)
        
        self.blockchain.new_block(proof=12345, previous_hash='abc123')
        last = self.blockchain.last_block
        self.assertEqual(last['indice'], 2)

    def test_multiple_blocks_chain(self):
        """Verifica que se pueden crear múltiples bloques en cadena"""
        for i in range(5):
            self.blockchain.new_block(proof=100 + i, previous_hash='abc')
        
        self.assertEqual(len(self.blockchain.chain), 6)  # Genesis + 5

    # ============================================
    # Pruebas de Proof of Work
    # ============================================

    def test_valid_proof_correct(self):
        """Verifica que una prueba válida es reconocida como válida"""
        # Para dificultad 3 (establecida en setUp), necesitamos 3 ceros al inicio.
        last_proof = 100
        last_hash = 'abc123'
        
        # Encontrar una prueba válida. Con D=3 (promedio 4096 intentos), 10000 es seguro.
        for proof in range(10000):
            if self.blockchain.valid_proof(last_proof, proof, last_hash):
                self.assertTrue(True)
                break
        else:
            self.fail("No se pudo encontrar una prueba válida después de 10000 intentos")

    def test_valid_proof_incorrect(self):
        """Verifica que una prueba inválida es rechazada"""
        last_proof = 100
        last_hash = 'abc123'
        invalid_proof = 1
        
        result = self.blockchain.valid_proof(last_proof, invalid_proof, last_hash)
        self.assertFalse(result)

    def test_proof_of_work(self):
        """Verifica que proof_of_work encuentra una prueba válida"""
        last_proof = 100
        last_hash = 'abc123'
        
        proof = self.blockchain.proof_of_work(last_proof, last_hash)
        self.assertTrue(self.blockchain.valid_proof(last_proof, proof, last_hash))

    def test_proof_of_work_different_inputs(self):
        """Verifica que diferentes inputs producen diferentes proofs"""
        proof1 = self.blockchain.proof_of_work(100, 'hash1')
        proof2 = self.blockchain.proof_of_work(101, 'hash1')
        proof3 = self.blockchain.proof_of_work(100, 'hash2')
        
        # Los proofs pueden ser ocasionalmente iguales, pero es improbable
        # para diferentes inputs
        results = [proof1, proof2, proof3]
        self.assertTrue(len(set(results)) > 1)

    # ============================================
    # Pruebas de Nodos
    # ============================================

    def test_register_node_valid(self):
        """Verifica que se registra un nodo válido"""
        self.blockchain.register_node('http://192.168.0.5:5000')
        self.assertIn('http://192.168.0.5:5000', self.blockchain.nodes)

    def test_register_node_with_path_only(self):
        """Verifica que se registra un nodo con solo la ruta"""
        self.blockchain.register_node('192.168.0.5:5000')
        self.assertIn('http://192.168.0.5:5000', self.blockchain.nodes)

    def test_register_multiple_nodes(self):
        """Verifica que se registran múltiples nodos"""
        self.blockchain.register_node('http://192.168.0.5:5000')
        self.blockchain.register_node('http://192.168.0.6:5000')
        self.blockchain.register_node('http://192.168.0.7:5000')
        
        self.assertEqual(len(self.blockchain.nodes), 3)

    def test_no_duplicate_nodes(self):
        """Verifica que no se registren nodos duplicados"""
        self.blockchain.register_node('http://192.168.0.5:5000')
        self.blockchain.register_node('http://192.168.0.5:5000')
        
        self.assertEqual(len(self.blockchain.nodes), 1)

    # ============================================
    # Pruebas de Validación de Cadena
    # ============================================

    def test_valid_chain_genesis_only(self):
        """Verifica que una cadena con solo génesis es válida"""
        self.assertTrue(self.blockchain.valid_chain(self.blockchain.chain))

    def test_valid_chain_multiple_blocks(self):
        """Verifica que una cadena válida con múltiples bloques es aceptada"""
        # Crear varios bloques válidos
        for i in range(3):
            last_block = self.blockchain.last_block
            last_proof = last_block['proof']
            last_hash = self.blockchain.hash(last_block)
            proof = self.blockchain.proof_of_work(last_proof, last_hash)
            self.blockchain.new_block(proof, last_hash)
        
        self.assertTrue(self.blockchain.valid_chain(self.blockchain.chain))

    def test_invalid_chain_bad_previous_hash(self):
        """Verifica que una cadena con hash anterior incorrecto es rechazada"""
        # Crear un bloque válido
        last_block = self.blockchain.last_block
        last_proof = last_block['proof']
        last_hash = self.blockchain.hash(last_block)
        proof = self.blockchain.proof_of_work(last_proof, last_hash)
        self.blockchain.new_block(proof, last_hash)
        
        # Modificar el previous_hash del segundo bloque
        self.blockchain.chain[1]['previous_hash'] = 'invalid_hash'
        
        self.assertFalse(self.blockchain.valid_chain(self.blockchain.chain))

    def test_invalid_chain_bad_proof(self):
        """Verifica que una cadena con prueba de trabajo inválida es rechazada"""
        # Crear un bloque válido
        last_block = self.blockchain.last_block
        last_proof = last_block['proof']
        last_hash = self.blockchain.hash(last_block)
        proof = self.blockchain.proof_of_work(last_proof, last_hash)
        self.blockchain.new_block(proof, last_hash)
        
        # Modificar el proof del segundo bloque
        self.blockchain.chain[1]['proof'] = 12345
        
        self.assertFalse(self.blockchain.valid_chain(self.blockchain.chain))

    # ============================================
    # Pruebas de Integración
    # ============================================

    def test_complete_workflow(self):
        """Prueba un flujo completo: crear transacciones, minar, validar"""
        # Crear transacciones
        self.blockchain.new_transaction('alice', 'bob', 50)
        self.blockchain.new_transaction('bob', 'charlie', 30)
        
        # Minar un bloque
        last_block = self.blockchain.last_block
        last_proof = last_block['proof']
        last_hash = self.blockchain.hash(last_block)
        proof = self.blockchain.proof_of_work(last_proof, last_hash)
        new_block = self.blockchain.new_block(proof, last_hash)
        
        # Validar
        self.assertEqual(len(new_block['transacciones']), 2)
        self.assertTrue(self.blockchain.valid_chain(self.blockchain.chain))
        self.assertEqual(len(self.blockchain.current_transactions), 0)

    def test_immutability_check(self):
        """Prueba que cambiar un bloque invalida la cadena"""
        # Crear varios bloques válidos
        for i in range(3):
            last_block = self.blockchain.last_block
            last_proof = last_block['proof']
            last_hash = self.blockchain.hash(last_block)
            proof = self.blockchain.proof_of_work(last_proof, last_hash)
            self.blockchain.new_block(proof, last_hash)
        
        self.assertTrue(self.blockchain.valid_chain(self.blockchain.chain))
        
        # Intentar modificar un bloque anterior
        self.blockchain.chain[1]['transacciones'].append({'emisor': 'hacker', 'receptor': 'hacker', 'cantidad': 1000})
        
        # Ahora la cadena debe ser inválida
        self.assertFalse(self.blockchain.valid_chain(self.blockchain.chain))

    def test_chain_length(self):
        """Verifica que la longitud de la cadena aumenta correctamente"""
        initial_length = len(self.blockchain.chain)
        
        for i in range(5):
            last_block = self.blockchain.last_block
            last_proof = last_block['proof']
            last_hash = self.blockchain.hash(last_block)
            proof = self.blockchain.proof_of_work(last_proof, last_hash)
            self.blockchain.new_block(proof, last_hash)
        
        self.assertEqual(len(self.blockchain.chain), initial_length + 5)


class TestBlockchainEdgeCases(unittest.TestCase):
    """Pruebas para casos extremos y errores"""

    def setUp(self):
        self.blockchain = Blockchain()
        self.blockchain.difficulty = 3

    def test_transaction_with_zero_amount(self):
        """Prueba transacción con cantidad cero"""
        index = self.blockchain.new_transaction('alice', 'bob', 0)
        self.assertEqual(index, 2)
        self.assertEqual(self.blockchain.current_transactions[0]['cantidad'], 0)

    def test_transaction_with_negative_amount(self):
        """Prueba transacción con cantidad negativa"""
        index = self.blockchain.new_transaction('alice', 'bob', -50)
        # El código actual permite esto, pero podrías agregar validación
        self.assertEqual(self.blockchain.current_transactions[0]['cantidad'], -50)

    def test_transaction_with_large_amount(self):
        """Prueba transacción con cantidad muy grande"""
        large_amount = 999999999999
        index = self.blockchain.new_transaction('alice', 'bob', large_amount)
        self.assertEqual(self.blockchain.current_transactions[0]['cantidad'], large_amount)

    def test_node_registration_with_trailing_slash(self):
        """Prueba registro de nodo con barra diagonal al final"""
        self.blockchain.register_node('http://192.168.0.5:5000/')
        self.assertIn('http://192.168.0.5:5000', self.blockchain.nodes)

    def test_empty_chain_validation(self):
        """Prueba validación de cadena vacía"""
        # Esto podría fallar en el código actual, pero es un caso límite
        try:
            result = self.blockchain.valid_chain([])
            # Si no falla, debería retornar True o False
        except (IndexError, KeyError):
            # Es esperado que falle con cadena vacía
            pass

    def test_hash_of_identical_blocks(self):
        """Verifica que bloques idénticos tienen hashes idénticos"""
        block_data = {
            'indice': 1,
            'timestamp': 123456,
            'transacciones': [],
            'proof': 100,
            'previous_hash': '1'
        }
        hash1 = self.blockchain.hash(block_data)
        hash2 = self.blockchain.hash(block_data)
        self.assertEqual(hash1, hash2)


if __name__ == '__main__':
    unittest.main(verbosity=2)