from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

g_key = get_random_bytes(16)
g_plaintext = b"abcdefghijklmnop"

def p_example5_nested_local_variable1(key, data):
    mode1 = AES.MODE_ECB
    mode2 = mode1
    mode3 = mode2

    cipher = AES.new(key, mode3)
    cipher_text = cipher.encrypt(data)
    return cipher_text

def decrypt_aes_ecb(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    cipher_text = cipher.decrypt(data)
    return cipher_text

if __name__ == '__main__':
    # TestRule1 code
    print("PyCrypto -> AESECB -> p_example5_nested_local_variable1:",
          decrypt_aes_ecb(g_key, p_example5_nested_local_variable1(g_key, g_plaintext)) == g_plaintext)
