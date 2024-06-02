from nacl.secret import SecretBox

g_nonce = b"123456781234567812345678"  # 24 byte
g_key = b"12345678123456781234567812345678"
nonce = b"123456781234567812345678"  # 24 byte
g_plaintext = b"abcdefghijklmnop"

def p_example5_nested_local_variable1(data):
    key1 = b"12345678123456781234567812345678"
    key2 = key1
    key3 = key2

    secret_box = SecretBox(key3)
    cipher_text = secret_box.encrypt(data, nonce)
    return cipher_text

def decrypt(key, data):
    secret_box = SecretBox(key)
    cipher_text = secret_box.decrypt(data, g_nonce)
    return cipher_text

if __name__ == '__main__':
    # TestRule3 code
    print("PyNaCl -> Key -> p_example5_nested_local_variable1:",
          decrypt(g_key, p_example5_nested_local_variable1(g_plaintext)[24:]) == g_plaintext)
