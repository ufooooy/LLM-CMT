from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

g_key = get_random_bytes(16)
g_iv = b"1234567812345678"
g_plaintext = b"abcdefghijklmnop"

def p_example_method_call(key, iv, data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(data)
    return cipher_text

def p_example7_direct_method_call1(key, data):
    iv = b"1234567812345678"
    return p_example_method_call(key, iv, data)

def decrypt_aes_cbc(key, iv, data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.decrypt(data)
    return cipher_text

if __name__ == '__main__':
    print("PyCrypto -> AESCBC -> p_example7_direct_method_call1:",
          decrypt_aes_cbc(g_key, g_iv, p_example7_direct_method_call1(g_key, g_plaintext)) == g_plaintext)
