import base64
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

g_backend = default_backend()
g_key = b"1234567812345678"
g_plaintext = b"abcdefghijklmnop"
g_key_fernet = base64.urlsafe_b64encode(b"12345678123456781234567812345678")

def p_example12_nested_local_variable4(data):
    key1 = base64.urlsafe_b64encode(bytes("12345678123456781234567812345678", "utf8"))
    key2 = key1
    key3 = key2

    fernet = Fernet(key3, backend=g_backend)
    cipher_text = fernet.encrypt(data)
    return cipher_text

def decrypt_fernet(key, data):
    fernet = Fernet(key)
    plaintext = fernet.decrypt(data)
    return plaintext

if __name__ == '__main__':
    print("cryptography -> p_example12_nested_local_variable4:",
          decrypt_fernet(g_key_fernet, p_example12_nested_local_variable4(g_plaintext)) == g_plaintext)
