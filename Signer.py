from cryptography.fernet import Fernet
import os
from platformdirs import user_documents_dir
from kyber_py.ml_kem import ML_KEM_1024
import hashlib
import base64
from dilithium_py.ml_dsa import ML_DSA_44

path = r'C:\Users\vboxuser\Documents\prueba.txt'

file = open(path,"rb")
hasher = hashlib.sha256()
data = file.read()
hasher.update(data)
hash = hasher.digest()
file.close()

pk, sk = ML_DSA_44.keygen() # public key, secret(private)key
digitalSignature = ML_DSA_44.sign(sk, hash)   # Uses the private key to encrypt the hash using sign(secret_key, message_bytes(the hash))

file = open("verificationKey.bin", "wb")
file.write(pk)  
file.close()

file = open("digitalSignature.bin", "wb")
file.write(digitalSignature)  
file.close()

