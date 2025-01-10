from Crypto.Cipher import AES

g_key = b"1234567812345678"
g_plaintext = b"abcdefghijklmnop"

def p_example6_nested_local_variable2(data):
    key1 = bytes("1234567812345678", "utf8")
    key2 = key1
    key3 = key2

    cipher = AES.new(key3, AES.MODE_ECB)
    cipher_text = cipher.encrypt(data)
    return cipher_text

def decrypt_aes_ecb(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    cipher_text = cipher.decrypt(data)
    return cipher_text

if __name__ == '__main__':
    print("PyCrypto -> Key -> p_example6_nested_local_variable2:",
          decrypt_aes_ecb(g_key, p_example6_nested_local_variable2(g_plaintext)) == g_plaintext)
