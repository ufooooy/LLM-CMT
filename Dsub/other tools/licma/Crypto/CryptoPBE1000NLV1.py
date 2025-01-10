import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

g_backend = default_backend()
g_password = b"12345678"
g_plaintext = b"abcdefghijklmnop"
g_salt = b"12345678"
g_iterations_lower_1000 = 999

def p_example3_nested_local_variable(password, data):
    count1 = 999
    count2 = count1
    count3 = count2

    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=16, salt=b"12345678", iterations=count3, backend=g_backend)
    key = kdf.derive(password)

    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=g_backend)
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(data) + encryptor.finalize()
    return cipher_text

def get_pbk(salt, iterations):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=16, salt=salt, iterations=iterations, backend=g_backend)
    key = kdf.derive(g_password)
    return key

def decrypt_aes_ecb(key, data):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=g_backend)
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(data) + decryptor.finalize()
    return plaintext

if __name__ == '__main__':
    print("cryptography -> PBE_iterations_lower_1000 -> p_example3_nested_local_variable:",
          decrypt_aes_ecb(get_pbk(g_salt, g_iterations_lower_1000),
                          p_example3_nested_local_variable(g_password, g_plaintext)) == g_plaintext)
