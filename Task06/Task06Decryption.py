from cryptography.fernet import Fernet
import os
from platformdirs import user_documents_dir
from pqc.kem import mceliece6960119 as eliece
import hashlib
import base64

def keyLoad(filename):
    with open(filename, "rb") as f:
        return f.read()

def decryption(password, folderpath):
    # 1. Generation of K2 with password
    salt = b""  # No salt 
    iterations = 100000
    dklen = 32 # dklen stands for desired key length. Fernet uses AES-128, but splits a 256 key in half, one for authentication

    key = hashlib.pbkdf2_hmac('sha256', password, salt, iterations, dklen)
    K2 = base64.urlsafe_b64encode(key)

    # 2. Reading and decryption of private Key (with K2)
    f2 = Fernet(K2)
    privateKey = f2.decrypt(keyLoad("privateKey.bin"))

    # 3. Reading and decryption of K1 (with private Key)
    encapK1 = keyLoad("encapK1.bin")
    K1 = eliece.decap(encapK1, privateKey)
    K1 = base64.urlsafe_b64encode(K1)
    # 4. Call to auxDecryption to recursively decrypt
    auxDecryption(K1,folderpath)

def auxDecryption(key, folderpath):
    f = Fernet(key)
    files = [file for file in os.listdir(folderpath) if not file.startswith('.') and file != 'desktop.ini' and not os.path.isjunction(os.path.join(folderpath, file)) and not os.path.islink(os.path.join(folderpath, file))]
    for filename in files:
        currentPath = os.path.join(folderpath, filename)
        if os.path.islink(currentPath):
        # ignores hidden links between Default folders
            continue
        if os.path.isfile(currentPath):
            # Binary reading of a given file
            with open (currentPath, "rb") as file:
                target = file.read()
            # Decryption of read file
            decryptedTarget = f.decrypt(target)
            # Overwrite of read file with its decryption
            with open(currentPath, "wb") as decryptedFile:
                decryptedFile.write(decryptedTarget)
        elif os.path.isdir(currentPath):
            auxDecryption(key,currentPath)

folderpath = user_documents_dir()
password = b"potato"
decryption(password,folderpath)