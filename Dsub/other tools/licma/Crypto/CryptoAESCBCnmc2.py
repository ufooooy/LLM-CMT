import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
g_backend = default_backend()
import os

g_key = os.urandom(16)
g_iv = b"1234567812345678"
g_plaintext = b"abcdefghijklmnop"

def p_example_method_call(key, iv, data):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=g_backend)
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(data) + encryptor.finalize()
    return cipher_text

def p_example_nested_method_call(key, iv, data):
    return p_example_method_call(key, iv, data)

def p_example10_nested_method_call2(key, data):
    iv = bytes("1234567812345678", "utf8")
    return p_example_nested_method_call(key, iv, data)

def decrypt_aes_cbc(key, iv, data):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=g_backend)
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(data) + decryptor.finalize()
    return plaintext

if __name__ == '__main__':
    print("cryptography -> AESCBC -> p_example10_nested_method_call2:",
          decrypt_aes_cbc(g_key, g_iv, p_example10_nested_method_call2(g_key, g_plaintext)) == g_plaintext)
