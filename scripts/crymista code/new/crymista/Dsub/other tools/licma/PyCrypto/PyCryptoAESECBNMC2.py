from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

g_key = get_random_bytes(16)
g_plaintext = b"abcdefghijklmnop"

def p_example_method_call(key, data, mode):
    cipher = AES.new(key, mode)
    cipher_text = cipher.encrypt(data)
    return cipher_text

def p_example_nested_method_call(key, data, mode):
    return p_example_method_call(key, data, mode)

def p_example10_nested_method_call2(key, data):
    mode = 1
    return p_example_nested_method_call(key, data, mode)

def decrypt_aes_ecb(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    cipher_text = cipher.decrypt(data)
    return cipher_text

if __name__ == '__main__':
    # TestRule1 code
    print("PyCrypto -> AESECB -> p_example10_nested_method_call2:",
          decrypt_aes_ecb(g_key, p_example10_nested_method_call2(g_key, g_plaintext)) == g_plaintext)
