from Crypto.Cipher import AES

g_key = b"1234567812345678"
g_plaintext = b"abcdefghijklmnop"
g_key1 = b"1234567812345678"
g_key2 = bytes("1234567812345678", "utf8")

def p_example14_indirect_g_variable_access2(data):
    key = g_key2
    cipher = AES.new(key, AES.MODE_ECB)
    cipher_text = cipher.encrypt(data)
    return cipher_text

def decrypt_aes_ecb(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    cipher_text = cipher.decrypt(data)
    return cipher_text

if __name__ == '__main__':
    print("PyCrypto -> Key -> p_example14_indirect_g_variable_access2:",
          decrypt_aes_ecb(g_key, p_example14_indirect_g_variable_access2(g_plaintext)) == g_plaintext)
