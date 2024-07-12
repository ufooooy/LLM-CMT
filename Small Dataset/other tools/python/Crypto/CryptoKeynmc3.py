import base64
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

g_backend = default_backend()
g_key = b"1234567812345678"
g_plaintext = b"abcdefghijklmnop"
g_key_fernet = base64.urlsafe_b64encode(b"12345678123456781234567812345678")

def p_example_method_call2(key, data):
    fernet = Fernet(key, backend=g_backend)
    cipher_text = fernet.encrypt(data)
    return cipher_text

def p_example_nested_method_call2(key, data):
    return p_example_method_call2(key, data)

def p_example19_nested_method_call3(data):
    key = base64.urlsafe_b64encode(b"12345678123456781234567812345678")
    return p_example_nested_method_call2(key, data)

def decrypt_fernet(key, data):
    fernet = Fernet(key)
    plaintext = fernet.decrypt(data)
    return plaintext

if __name__ == '__main__':
    print("cryptography -> p_example19_nested_method_call3:",
          decrypt_fernet(g_key_fernet, p_example19_nested_method_call3(g_plaintext)) == g_plaintext)
