from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

g_backend = default_backend()
g_key = b"1234567812345678"
g_plaintext = b"abcdefghijklmnop"

def p_example10_nested_local_variable2(data):
    key1 = bytes("1234567812345678", "utf8")
    key2 = key1
    key3 = key2

    cipher = Cipher(algorithms.AES(key3), modes.ECB(), backend=g_backend)
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(data) + encryptor.finalize()
    return cipher_text

def decrypt_aes_ecb(key, data):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=g_backend)
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(data) + decryptor.finalize()
    return plaintext

if __name__ == '__main__':
    print("cryptography -> p_example10_nested_local_variable2:",
          decrypt_aes_ecb(g_key, p_example10_nested_local_variable2(g_plaintext)) == g_plaintext)
