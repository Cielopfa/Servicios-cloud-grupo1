import requests
import time
import json
import os 

API = 'http://localhost:5000'

def clear_screen():
    # Limpia la consola
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception:
        pass

def wait_for_continue():
    # Espera para que el usuario pueda leer la explicación
    input('\nPresione Enter para volver al menú...')


def mostrar_menu():
    clear_screen()
    print('\nJuego Educativo - Blockchain (5 niveles)')
    print('Elige una acción para explorar un concepto clave:')
    print('1. Nivel 1 - Fundamentos (Ver cadena y estructura del bloque)')
    print('2. Nivel 2 - Transacciones (Crear, agrupar y ver su estado)')
    print('3. Nivel 3 - Prueba de Trabajo y Minado')
    print('4. Nivel 4 - Inmutabilidad (Inspeccionar hashes y seguridad)')
    print('5. Nivel 5 - Consenso distribuido (Simular nodos y la regla de la cadena más larga)')
    print('0. Salir')


def nivel1():
    clear_screen()
    print('\n--- Nivel 1: Fundamentos de la Cadena (Bloques y Estructura) ---')
    print('Objetivo: Entender que una Blockchain es una lista enlazada de bloques.')
    
    try:
        resp = requests.get(f'{API}/cadena', timeout=3)
        resp.raise_for_status()
        data = resp.json()
        print(f'\nCadena descargada. Longitud actual: {len(data["cadena"])}')
        
        for b in data['cadena']:
            print('\n' + '=' * 40)
            print(f"Bloque {b['indice']}")
            print(f"Timestamp: {time.ctime(b['timestamp'])}")
            print(f"Transacciones: {len(b['transacciones'])}")
            print(f"Proof (Prueba de Trabajo): {b['proof']}")
            print(f"Previous Hash (Hash del Bloque Anterior): {b['previous_hash']}")
            print('=' * 40)
            print('Concepto Clave: El `previous_hash` es el enlace criptográfico que garantiza el orden y la integridad')
        
    except requests.RequestException:
        print('\nError: No se pudo conectar al servidor. Asegúrese de que esté activo.')

    wait_for_continue()


def nivel2():
    clear_screen()
    print('\n--- Nivel 2: Transacciones (Creación y Estado) ---')
    print('Objetivo: Entender que las transacciones son operaciones que se agrupan en una lista de espera (mempool) antes de ser incluidas en un bloque.')
    
    try:
        emisor = input('Emisor (ej: alice): ')
        receptor = input('Receptor (ej: bob): ')
        
        while True:
            try:
                cantidad = int(input('Cantidad (entero): '))
                break
            except ValueError:
                print('Por favor, introduzca un número entero válido.')
                
        payload = {'emisor': emisor, 'receptor': receptor, 'cantidad': cantidad}
        resp = requests.post(f'{API}/transacciones/nueva', json=payload, timeout=3)
        resp.raise_for_status()
        
        respuesta = resp.json()
        print('\nRespuesta del Servidor:')
        print(f"Mensaje: {respuesta.get('mensaje')}")
        print('Concepto Clave: La transacción está ahora en la lista de espera y solo se confirmará cuando un minero la incluya en un bloque.')
        
    except requests.RequestException:
        print('\nError: No se pudo enviar la transacción al servidor')
    except Exception as e:
        print(f'Ocurrió un error: {e}')
        
    wait_for_continue()


def nivel3():
    clear_screen()
    print('\n--- Nivel 3: Prueba de Trabajo y Minado ---')
    print('Objetivo: Entender que el Minado es el proceso de resolver la Prueba de Trabajo (PoW) para validar transacciones y asegurar el bloque.')
    
    try:
        print('\nIniciando minado... el servidor está buscando un número ("nonce") cuyo hash cumpla la dificultad (ej: inicie con varios ceros). Esto puede tardar varios segundos.')
        resp = requests.get(f'{API}/minar', timeout=60)
        resp.raise_for_status()
        
        respuesta = resp.json()
        print('\n--- Bloque Minado con Éxito ---')
        print(f"Mensaje: {respuesta.get('mensaje')}")
        print(f"Número de Bloque: {respuesta.get('indice_nuevo')}")
        print(f"Proof encontrado: {respuesta.get('proof')}")
        print('Concepto Clave: El minero recibe una recompensa por el esfuerzo computacional que verifica la red. Esto incentiva la seguridad y la creación de bloques.')
        
    except requests.exceptions.Timeout:
        print('\nEl minado ha excedido el tiempo de espera. La Prueba de Trabajo puede ser muy difícil.')
    except requests.RequestException:
        print('\nError: No se pudo contactar al servidor o el minado falló.')
        
    wait_for_continue()


def nivel4():
    clear_screen()
    print('\n--- Nivel 4: Inmutabilidad (Inspección de Hashes) ---')
    print('Objetivo: Entender que la Inmutabilidad se logra porque cualquier alteración en el bloque cambia su hash, invalidando todos los bloques siguientes.')
    
    try:
        print('\nDescargando cadena para inspección...')
        resp = requests.get(f'{API}/cadena', timeout=3)
        resp.raise_for_status()
        data = resp.json()
        
        print('\n--- Inspección del Primer Bloque (Génesis) ---')
        genesis = data['cadena'][0]
        print(f"Índice: {genesis['indice']}")
        print(f"Timestamp: {time.ctime(genesis['timestamp'])}")
        print(f"Transacciones: {genesis['transacciones']}")
        
        if len(data['cadena']) > 1:
            print('\n--- Inspección del Segundo Bloque ---')
            segundo = data['cadena'][1]
            print(f"Hash anterior (previous_hash): {segundo['previous_hash']}")
            print('Concepto Clave: Este hash debe coincidir exactamente con el hash calculado del bloque anterior (génesis).')
            print('Si se intentara cambiar un dato en el Bloque 1, su hash cambiaría, y el Bloque 2 se volvería inválido, rompiendo la cadena.')
        else:
            print('\nNo hay suficientes bloques para demostrar la cadena de hashes. Mine más bloques.')

    except requests.RequestException:
        print('\nError: No se pudo descargar la cadena.')

    wait_for_continue()


def nivel5():
    clear_screen()
    print('\n--- Nivel 5: Consenso distribuido (Simulación de Nodos) ---')
    print('Objetivo: Entender que el Consenso es el mecanismo para que todos los nodos de la red estén de acuerdo en la única cadena válida')
    
    try:
        print('\n1. Registrando un nodo de ejemplo para simular la red.')
        nodo = input('URL del nodo a registrar (ej: http://localhost:5001): ')
        resp = requests.post(f'{API}/nodos/registrar', json={'nodos': [nodo]}, timeout=3)
        print(f"Registro: {resp.json()}")
        
        print('\n2. Ejecutando el algoritmo de Consenso (Resolución de Conflictos)...')
        time.sleep(1)
        resp2 = requests.get(f'{API}/nodos/resolver', timeout=5)
        resp2.raise_for_status()
        
        respuesta2 = resp2.json()
        print(f"Resultado del Consenso: {respuesta2.get('mensaje')}")
        if 'nueva_cadena' in respuesta2:
            print(f"Longitud de la cadena adoptada: {len(respuesta2['nueva_cadena'])}")
            
        print('Concepto Clave: El algoritmo busca la cadena más larga entre todos los nodos. Si la local es más corta, se reemplaza. Así se garantiza una única verdad distribuida.')

    except requests.RequestException:
        print('\nError en la comunicación con el servidor o durante el consenso.')
        
    wait_for_continue()


def main():
    while True:
        mostrar_menu()
        opc = input('Elija nivel: ')
        
        if opc == '1':
            nivel1()
        elif opc == '2':
            nivel2()
        elif opc == '3':
            nivel3()
        elif opc == '4':
            nivel4()
        elif opc == '5':
            nivel5()
        elif opc == '0':
            print('Saliendo...')
            break
        else:
            print('Opción inválida')


if __name__ == '__main__':
    print('Asegúrese de que `blockchain.py` esté corriendo en http://localhost:5000')
    main()