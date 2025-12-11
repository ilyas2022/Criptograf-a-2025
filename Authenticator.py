from cryptography.fernet import Fernet
import os
from platformdirs import user_documents_dir
from mceliece_kem import ML_MCELIECE_1024_CLASS as ML_KEM_1024
import hashlib
import base64
from dilithium_py.ml_dsa import ML_DSA_44

def keyLoad(filename):
    with open(filename, "rb") as f:
        return f.read()

pk = keyLoad("verificationKey.bin")
digitalSignature = keyLoad("digitalSignature.bin")

path = r'C:\Users\vboxuser\Documents\prueba.txt'

file = open(path,"rb")
hasher = hashlib.sha256()
data = file.read()
hasher.update(data)
hash = hasher.digest()
file.close()

is_valid = ML_DSA_44.verify(pk, hash, digitalSignature)  # verify(public_key, message_bytes, signature)
print("Validity: ", is_valid)