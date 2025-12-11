"""
from pqcrypto.kem.mceliece6960119 import *
print("ok")
publicKey, privateKey = generate_keypair()
K1,encapK1 = encrypt(publicKey)
K1 = decrypt(encapK1,privateKey)
"""
from pqc.kem import mceliece6960119 as eliece

publicKey, privateKey = eliece.keypair()
K1, encapK1 = eliece.encap(publicKey)
K1 = eliece.decap(encapK1, privateKey)
print("ok")