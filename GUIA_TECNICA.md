# Guía Técnica

Documento técnico que explica la implementación detallada del proyecto "Blockchain Educativo con Python".

## Estructura de Bloques
Cada bloque implementado contiene los siguientes campos:

- `indice`: posición en la cadena
- `timestamp`: marca de tiempo en segundos
- `transacciones`: lista de transacciones incluidas
- `proof`: número que satisface la prueba de trabajo
- `previous_hash`: hash SHA-256 del bloque anterior

## Hash SHA-256
Se utiliza la librería `hashlib` para generar hashes SHA-256 a partir de una representación JSON ordenada del bloque.

## Prueba de Trabajo (PoW)
El algoritmo implementado busca un `proof` tal que SHA256(last_proof + proof + last_hash) comience con N ceros, donde N es `difficulty` (por defecto 4).

## Consenso Distribuido
Para resolver conflictos, cada nodo descarga la cadena de sus vecinos, valida su integridad y adopta la cadena más larga válida.

## Persistencia
Actualmente la cadena se mantiene en memoria. Extensiones futuras: persistir en archivo JSON o base de datos ligera (SQLite).

## Extensiones recomendadas
- Firmas digitales con `ecdsa` o `cryptography` para autenticar transacciones.
- Árboles de Merkle para optimizar la verificación de transacciones.
- Ajuste dinámico de dificultad similar a Bitcoin.
- Persistencia y recuperación de estado.

## Ejecución en la nube
Puedes contenerizar la aplicación con Docker y desplegar en servicios como Azure Container Instances o App Service. Añadir variables de entorno para configuración de puertos y dificultad.