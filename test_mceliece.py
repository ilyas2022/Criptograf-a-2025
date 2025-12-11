"""
Test script for McEliece KEM implementation
"""

from mceliece_kem import ML_MCELIECE_1024_CLASS as ML_KEM

print("Testing McEliece KEM Implementation")
print("=" * 50)

# Test 1: Key Generation
print("\n1. Testing key generation...")
try:
    public_key, private_key = ML_KEM.keygen()
    print(f"   ✓ Public key size: {len(public_key)} bytes")
    print(f"   ✓ Private key size: {len(private_key)} bytes")
except Exception as e:
    print(f"   ✗ Error: {e}")
    exit(1)

# Test 2: Encapsulation
print("\n2. Testing encapsulation...")
try:
    shared_secret1, ciphertext = ML_KEM.encaps(public_key)
    print(f"   ✓ Shared secret size: {len(shared_secret1)} bytes")
    print(f"   ✓ Ciphertext size: {len(ciphertext)} bytes")
    print(f"   ✓ Shared secret (first 16 bytes): {shared_secret1[:16].hex()}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    exit(1)

# Test 3: Decapsulation
print("\n3. Testing decapsulation...")
try:
    shared_secret2 = ML_KEM.decaps(private_key, ciphertext)
    print(f"   ✓ Recovered secret size: {len(shared_secret2)} bytes")
    print(f"   ✓ Recovered secret (first 16 bytes): {shared_secret2[:16].hex()}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    exit(1)

# Test 4: Verify shared secrets match
print("\n4. Verifying shared secrets match...")
if shared_secret1 == shared_secret2:
    print("   ✓ SUCCESS! Shared secrets match perfectly!")
else:
    print("   ✗ FAILURE! Shared secrets do not match")
    print(f"   Original:  {shared_secret1.hex()}")
    print(f"   Recovered: {shared_secret2.hex()}")
    exit(1)

# Test 5: Multiple iterations
print("\n5. Testing multiple encaps/decaps cycles...")
success_count = 0
total_tests = 10
for i in range(total_tests):
    pk, sk = ML_KEM.keygen()
    secret1, ct = ML_KEM.encaps(pk)
    secret2 = ML_KEM.decaps(sk, ct)
    if secret1 == secret2:
        success_count += 1

print(f"   ✓ Success rate: {success_count}/{total_tests} ({100*success_count/total_tests:.1f}%)")

if success_count == total_tests:
    print("\n" + "=" * 50)
    print("ALL TESTS PASSED! McEliece KEM is working correctly.")
    print("=" * 50)
else:
    print("\n" + "=" * 50)
    print(f"WARNING: Only {success_count}/{total_tests} tests passed.")
    print("=" * 50)
