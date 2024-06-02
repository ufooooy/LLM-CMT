from Crypto.Cipher import AES

g_key = b"1234567812345678"
g_plaintext = b"abcdefghijklmnop"

def p_example_method_call(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    cipher_text = cipher.encrypt(data)
    return cipher_text

def p_example7_direct_method_call1(data):
    key = b"1234567812345678"
    return p_example_method_call(key, data)

def decrypt_aes_ecb(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    cipher_text = cipher.decrypt(data)
    return cipher_text

if __name__ == '__main__':
    print("PyCrypto -> Key -> p_example7_direct_method_call1:",
          decrypt_aes_ecb(g_key, p_example7_direct_method_call1(g_plaintext)) == g_plaintext)
