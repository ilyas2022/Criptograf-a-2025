import hashlib
import base64

import tkinter as tk
from tkinter import filedialog


password = b"potato"
salt = b""  # No salt 
iterations = 100000
dklen = 32 # dklen stands for desired key length. Fernet uses AES-128, but splits a 256 key in half, one for authentication

key = hashlib.pbkdf2_hmac('sha256', password, salt, iterations, dklen)
K2 = base64.urlsafe_b64encode(key).decode()

print("PBKDF2 derived key (base64):", K2)


root = tk.Tk()
root.withdraw()  # Hide the root window

file_path = filedialog.askopenfilename(title="Select a file")
print("Selected file:", file_path)

