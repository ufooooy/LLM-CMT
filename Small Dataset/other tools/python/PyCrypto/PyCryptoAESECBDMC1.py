from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

g_key = get_random_bytes(16)
g_plaintext = b"abcdefghijklmnop"

def p_example_method_call(key, data, mode):
    cipher = AES.new(key, mode)
    cipher_text = cipher.encrypt(data)
    return cipher_text

def p_example7_direct_method_call1(key, data):
    mode = AES.MODE_ECB
    return p_example_method_call(key, data, mode)

def decrypt_aes_ecb(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    cipher_text = cipher.decrypt(data)
    return cipher_text

if __name__ == '__main__':
    # TestRule1 code
    print("PyCrypto -> AESECB -> p_example7_direct_method_call1:",
          decrypt_aes_ecb(g_key, p_example7_direct_method_call1(g_key, g_plaintext)) == g_plaintext)
