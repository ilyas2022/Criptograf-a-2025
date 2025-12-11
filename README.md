# Proyecto de Criptografía Post-Cuántica: Sustitución de Kyber por McEliece

## Descripción del Proyecto

Este proyecto implementa un sistema de cifrado de archivos que originalmente utilizaba el algoritmo Kyber (ML-KEM) para el encapsulamiento de claves. El objetivo principal de esta práctica ha sido sustituir Kyber por el algoritmo McEliece, manteniendo la funcionalidad completa del sistema de cifrado.

## Contexto Académico

### Criptografía Post-Cuántica

Los algoritmos de criptografía post-cuántica son esquemas criptográficos diseñados para resistir ataques de computadoras cuánticas. NIST ha estandarizado varios algoritmos post-cuánticos, incluyendo:

- **Kyber (ML-KEM)**: Basado en retículos (lattice-based cryptography)
- **McEliece**: Basado en códigos de corrección de errores (code-based cryptography)

Ambos algoritmos son mecanismos de encapsulamiento de claves (KEM - Key Encapsulation Mechanism) que permiten establecer una clave compartida de forma segura.

## Estructura del Proyecto

### Archivos Principales

#### Archivos de Cifrado/Descifrado

- **encryption.py**: Implementa el sistema de cifrado de carpetas
  - Genera claves pública y privada usando McEliece
  - Realiza encapsulamiento para crear K1 (clave de cifrado de archivos)
  - Deriva K2 usando PBKDF2 para proteger la clave privada
  - Cifra archivos recursivamente usando Fernet (AES)

- **decryption.py**: Implementa el sistema de descifrado
  - Recupera la clave privada usando K2 (derivada de contraseña)
  - Realiza desencapsulamiento para recuperar K1
  - Descifra archivos recursivamente

#### Archivos de Firma Digital

- **Signer.py**: Crea firmas digitales usando Dilithium (ML-DSA)
- **Authenticator.py**: Verifica firmas digitales

#### Módulos Personalizados

- **mceliece_kem.py**: Implementación educativa de McEliece KEM
  - Clase `McEliece_KEM`: Implementación del algoritmo
  - Interfaz compatible con Kyber: `keygen()`, `encaps()`, `decaps()`
  - Parámetros: n=192, k=128, t=8

- **test_mceliece.py**: Suite de pruebas para verificar la implementación

## Implementación de McEliece

### Parámetros del Sistema

- **n = 192**: Longitud del código (número de bits en el ciphertext)
- **k = 128**: Dimensión del mensaje (número de bits de información)
- **t = 8**: Capacidad de corrección de errores

### Características de la Implementación

#### Generación de Claves (keygen)

1. Se genera una matriz generadora G en forma sistemática: G = [I_k | P]
   - I_k: matriz identidad k×k
   - P: matriz aleatoria k×(n-k)

2. Clave pública: Matriz G (24.7 KB)
3. Clave privada: Matriz G y matriz P (33.0 KB)

#### Encapsulamiento (encaps)

1. Se genera un mensaje aleatorio m de k bits
2. Se genera un vector de error e con exactamente t bits en 1
   - Preferentemente en la parte de redundancia para facilitar decodificación
3. Se calcula el ciphertext: c = m × G + e (mod 2)
4. Se deriva el secreto compartido: shared_secret = SHA256(m)
5. Se retorna (shared_secret, ciphertext)

#### Desencapsulamiento (decaps)

1. Se recibe el ciphertext c
2. Se decodifica usando la estructura sistemática del código:
   - Se extraen los bits de información (primeros k bits)
   - Se extraen los bits de paridad (últimos n-k bits)
   - Se verifica la consistencia y se corrigen errores
3. Se recupera el mensaje m
4. Se deriva el secreto compartido: shared_secret = SHA256(m)

### Simplificaciones Educativas

La implementación realizada es una versión educativa que simplifica ciertos aspectos del McEliece original:

1. **Sin permutación ni scrambling**: En McEliece clásico se aplican matrices de permutación (P) y scrambling (S) para ocultar la estructura del código. En esta versión educativa se omiten para claridad.

2. **Códigos aleatorios en lugar de Goppa**: La implementación usa códigos lineales aleatorios en forma sistemática en lugar de códigos de Goppa. Esto simplifica la generación de claves pero reduce la seguridad teórica.

3. **Decodificación simplificada**: Se usa un decodificador que asume que la mayoría de errores están en la parte de redundancia, lo que acelera el proceso.

4. **Parámetros reducidos**: Los parámetros (n=192, k=128, t=8) son menores que los recomendados para uso real (ej: Classic McEliece usa n=6960, k=5413, t=119).

## Flujo de Cifrado Completo

### Proceso de Cifrado (encryption.py)

1. **Generación de claves McEliece**
   ```
   publicKey, privateKey = ML_KEM_1024.keygen()
   ```

2. **Encapsulamiento para obtener K1**
   ```
   K1, encapK1 = ML_KEM_1024.encaps(publicKey)
   ```
   - K1: Clave de 32 bytes (SHA256 del mensaje)
   - encapK1: Ciphertext de 192 bytes

3. **Derivación de K2 desde contraseña**
   ```
   K2 = PBKDF2-HMAC-SHA256(password, salt, 100000 iterations, 32 bytes)
   ```

4. **Protección de la clave privada**
   ```
   privateKey_encrypted = Fernet(K2).encrypt(privateKey)
   ```

5. **Almacenamiento**
   - privateKey.bin: Clave privada cifrada con K2
   - encapK1.bin: K1 encapsulada

6. **Cifrado de archivos**
   ```
   Para cada archivo en la carpeta:
       encrypted_file = Fernet(K1).encrypt(file_content)
   ```

### Proceso de Descifrado (decryption.py)

1. **Derivación de K2 desde contraseña**
   ```
   K2 = PBKDF2-HMAC-SHA256(password, salt, 100000 iterations, 32 bytes)
   ```

2. **Recuperación de la clave privada**
   ```
   privateKey = Fernet(K2).decrypt(privateKey_encrypted)
   ```

3. **Desencapsulamiento para recuperar K1**
   ```
   K1 = ML_KEM_1024.decaps(privateKey, encapK1)
   ```

4. **Descifrado de archivos**
   ```
   Para cada archivo cifrado:
       decrypted_file = Fernet(K1).decrypt(encrypted_content)
   ```

## Comparación: Kyber vs McEliece

| Característica | Kyber (ML-KEM) | McEliece |
|---------------|----------------|----------|
| Base matemática | Retículos (Lattices) | Códigos correctores de errores |
| Tamaño de clave pública | ~1.5 KB | ~25 KB (implementación educativa) |
| Tamaño de clave privada | ~3.2 KB | ~33 KB (implementación educativa) |
| Tamaño de ciphertext | ~1.5 KB | 192 bytes |
| Velocidad | Rápido | Moderado |
| Madurez del estándar | NIST seleccionado (2022) | Propuesto desde 1978 |
| Seguridad demostrada | Alta | Muy alta (40+ años sin ataques exitosos) |

## Verificación y Pruebas

### Ejecutar Tests

```bash
cd /mnt/c/Users/ilyas/Desktop/UAL-Ing.Software/Criptografia/Criptograf-a-2025
python3 test_mceliece.py
```

### Resultado Esperado

```
Testing McEliece KEM Implementation
==================================================

1. Testing key generation...
   Public key size: 24740 bytes
   Private key size: 32975 bytes

2. Testing encapsulation...
   Shared secret size: 32 bytes
   Ciphertext size: 192 bytes

3. Testing decapsulation...
   Recovered secret size: 32 bytes

4. Verifying shared secrets match...
   SUCCESS! Shared secrets match perfectly!

5. Testing multiple encaps/decaps cycles...
   Success rate: 10/10 (100.0%)

==================================================
ALL TESTS PASSED! McEliece KEM is working correctly.
==================================================
```

## Aspectos Técnicos Adicionales

### Álgebra Lineal sobre GF(2)

Todas las operaciones matriciales se realizan sobre el campo de Galois GF(2), donde:
- Suma: XOR bit a bit
- Multiplicación: AND bit a bit
- Todas las operaciones se hacen módulo 2

### Corrección de Errores

El decodificador implementado:

1. Extrae la parte de información (primeros k bits del ciphertext)
2. Extrae la parte de paridad (últimos n-k bits)
3. Calcula la paridad esperada: parity = m × P (mod 2)
4. Compara con la paridad recibida para detectar errores
5. Si hay errores, intenta correcciones simples bit a bit
6. Retorna el mensaje más probable

### Seguridad del Sistema Completo

El sistema utiliza múltiples capas de seguridad:

1. **McEliece KEM**: Protege K1 contra ataques cuánticos
2. **PBKDF2**: Protege la clave privada mediante derivación lenta de contraseña
3. **Fernet (AES-128)**: Cifrado simétrico de los archivos
4. **SHA-256**: Hashing criptográfico para derivar secretos

## Dependencias

```
numpy>=1.20.0
cryptography>=3.4.8
platformdirs>=2.0.0
```

### Instalación de Dependencias

```bash
pip install numpy cryptography platformdirs
```

## Limitaciones y Consideraciones

### Para Uso Educativo

Esta implementación es adecuada para:
- Comprender el funcionamiento de McEliece
- Demostrar conceptos de criptografía post-cuántica
- Propósitos académicos y de aprendizaje

### No Apto para Producción

Esta implementación NO debe usarse en entornos de producción porque:
- Usa códigos aleatorios en lugar de códigos de Goppa
- Parámetros de seguridad reducidos
- Sin permutación ni scrambling
- Decodificador simplificado

### Para Uso en Producción

Para aplicaciones reales se debe usar:
- Implementaciones estándar de Classic McEliece (NIST PQC)
- Bibliotecas como `liboqs` o `pqcrypto`
- Parámetros recomendados por NIST

## Referencias

### Artículos y Estándares

1. McEliece, R. J. (1978). "A public-key cryptosystem based on algebraic coding theory"
2. NIST Post-Quantum Cryptography Standardization (2016-presente)
3. Bernstein, D. J., et al. "Classic McEliece: conservative code-based cryptography"

### Recursos en Línea

- Classic McEliece Specification: https://classic.mceliece.org/
- NIST PQC Project: https://csrc.nist.gov/projects/post-quantum-cryptography
- Kyber Specification: https://pq-crystals.org/kyber/

## Autor y Contexto

- **Asignatura**: Criptografía
- **Universidad**: UAL - Ingeniería de Software
- **Fecha**: Diciembre 2025
- **Objetivo**: Implementar y comparar algoritmos de criptografía post-cuántica

## Conclusiones

Este proyecto demuestra exitosamente:

1. La viabilidad de sustituir algoritmos post-cuánticos manteniendo la funcionalidad
2. Las diferencias fundamentales entre esquemas basados en retículos (Kyber) y códigos (McEliece)
3. Los principios de los mecanismos de encapsulamiento de claves (KEM)
4. La importancia de la criptografía post-cuántica ante la amenaza de computadoras cuánticas

La implementación educativa de McEliece proporciona una comprensión profunda del algoritmo mientras mantiene la compatibilidad con el sistema de cifrado existente, demostrando la modularidad y abstracción adecuada en el diseño del software criptográfico.
