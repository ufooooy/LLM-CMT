from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

g_key = get_random_bytes(16)
g_plaintext = b"abcdefghijklmnop"
g_mode1 = AES.MODE_ECB
g_mode2 = 1

def p_example11_direct_g_variable_access1(key, data):
    cipher = AES.new(key, g_mode1)
    cipher_text = cipher.encrypt(data)
    return cipher_text

def decrypt_aes_ecb(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    cipher_text = cipher.decrypt(data)
    return cipher_text

if __name__ == '__main__':
    # TestRule1 code
    print("PyCrypto -> AESECB -> p_example11_direct_g_variable_access1:",
          decrypt_aes_ecb(g_key, p_example11_direct_g_variable_access1(g_key, g_plaintext)) == g_plaintext)