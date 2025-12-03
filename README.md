# Blockchain Educativo con Python
Implementación completa de una blockchain educativa distribuida desde cero usando Python, Flask y sockets/HTTP. Proyecto educativo que demuestra los conceptos fundamentales de blockchain mediante un juego interactivo.

## Descripción del Proyecto
Este proyecto implementa un sistema blockchain funcional que cumple con los requisitos técnicos:

- Red blockchain distribuida desde cero
- Python y Flask como tecnologías base
- Hash SHA-256 para integridad criptográfica
- Prueba de trabajo (PoW) como algoritmo de consenso
- HTTP para comunicación entre nodos
- JSON para serialización de datos

## Componentes implementados
- Estructura de bloques: índice, timestamp, transacciones, prueba (PoW) y hash anterior.
- Encadenamiento criptográfico con SHA-256.
- Pool de transacciones pendientes que se confirman al minar.
- Minado con dificultad configurable (por defecto 4 ceros).
- Consenso distribuido: regla de la cadena más larga.
- Red de nodos: registro y resolución de conflictos.

## Requisitos del Sistema
- Python 3.7 o superior
- pip

## Instalación
1. Clonar o Descargar el Proyecto

2. Instalar dependencias

```
pip install -r requirements.txt
```

## Estructura del Proyecto

```
Sistemas-operativos-/
│
├── blockchain.py           # Implementación principal del blockchain
├── juego_educativo.py      # Interfaz interactiva educativa
├── test_blockchain.py      # Suite de pruebas automáticas
├── requirements.txt        # Dependencias del proyecto
├── README.md               # Documentación principal
└── GUIA_TECNICA.md         # Guía técnica detallada
```

## Guía de uso

Modo 1: Sistema Básico
```
python blockchain.py
```
El servidor iniciará en http://localhost:5000

Ver blockchain: `http://localhost:5000/cadena`
Minar bloque: `http://localhost:5000/minar`
Información del nodo: `http://localhost:5000/`

Modo 2: Juego Educativo Interactivo (RECOMENDADO)

Terminal 1: Iniciar servidor

```
python blockchain.py
```

Terminal 2: Iniciar juego

```
python juego_educativo.py
```

Modo 3: Pruebas Automáticas

```
python test_blockchain.py
```

Modo 4: Red Distribuida (Avanzado)

Ejecutar múltiples nodos en distintos puertos:

```
python blockchain.py -p 5000
python blockchain.py -p 5001
python blockchain.py -p 5002
```

Registrar nodos entre sí (usar curl o Postman):

```
POST http://localhost:5000/nodos/registrar
Content-Type: application/json

{
  "nodos": ["http://localhost:5001", "http://localhost:5002"]
}
```

Ejecutar consenso:

```
GET http://localhost:5000/nodos/resolver
```

## Endpoints API REST

- GET `/` : Información básica del nodo
- GET `/cadena` : Obtiene la blockchain completa
- GET `/minar` : Mina un nuevo bloque
- POST `/transacciones/nueva` : Crear nueva transacción
- POST `/nodos/registrar` : Registrar nodos
- GET `/nodos/resolver` : Ejecutar algoritmo de consenso

## Limitaciones
Proyecto educativo, no para producción: sin persistencia, sin firmas digitales, sin protección avanzada.