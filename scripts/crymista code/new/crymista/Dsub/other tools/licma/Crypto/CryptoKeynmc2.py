from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

g_backend = default_backend()
g_key = b"1234567812345678"
g_plaintext = b"abcdefghijklmnop"

def p_example_method_call1(key, data):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=g_backend)
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(data) + encryptor.finalize()
    return cipher_text

def p_example_nested_method_call1(key, data):
    return p_example_method_call1(key, data)

def p_example18_nested_method_call2(data):
    key = bytes("1234567812345678", "utf8")
    return p_example_nested_method_call1(key, data)

def decrypt_aes_ecb(key, data):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=g_backend)
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(data) + decryptor.finalize()
    return plaintext

if __name__ == '__main__':
    print("cryptography -> p_example18_nested_method_call2:",
          decrypt_aes_ecb(g_key, p_example18_nested_method_call2(g_plaintext)) == g_plaintext)
