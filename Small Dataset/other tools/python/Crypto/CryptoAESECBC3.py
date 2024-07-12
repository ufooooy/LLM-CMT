from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

g_backend = default_backend()
import os

g_key = os.urandom(16)
g_plaintext = b"abcdefghijklmnop"
def decrypt_aes_ecb(key, data):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=g_backend)
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(data) + decryptor.finalize()
    return plaintext

def p_example3_nested_local_variable(key, data):
    mode1 = modes.ECB()
    mode2 = mode1
    mode3 = mode2
    cipher = Cipher(algorithms.AES(key), mode3, backend=g_backend)
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(data) + encryptor.finalize()
    return cipher_text


if __name__ == '__main__':
    # TestRule1 code
    print("cryptography -> AESECB_example3_nested_local_variable:",
          decrypt_aes_ecb(g_key, p_example3_nested_local_variable(g_key, g_plaintext)) == g_plaintext)
