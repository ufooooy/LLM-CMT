from Crypto.Cipher import AES

g_key = b"1234567812345678"
g_plaintext = b"abcdefghijklmnop"

def p_example_method_call(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    cipher_text = cipher.encrypt(data)
    return cipher_text

def p_example_nested_method_call(key, data):
    return p_example_method_call(key, data)

def p_example10_nested_method_call2(data):
    key = bytes("1234567812345678", "utf8")
    return p_example_nested_method_call(key, data)

def decrypt_aes_ecb(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    cipher_text = cipher.decrypt(data)
    return cipher_text

if __name__ == '__main__':
    print("PyCrypto -> Key -> p_example10_nested_method_call2:",
          decrypt_aes_ecb(g_key, p_example10_nested_method_call2(g_plaintext)) == g_plaintext)
