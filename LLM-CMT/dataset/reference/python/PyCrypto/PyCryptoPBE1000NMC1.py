from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

g_password = "12345678"
g_plaintext = b"abcdefghijklmnop"
g_count_lower_1000 = 999
g_salt = b"12345678"

def p_example_method_call(password, count, data):
    key = PBKDF2(password, b"12345678", 16, count=count)
    cipher = AES.new(key, AES.MODE_ECB)
    cipher_text = cipher.encrypt(data)
    return cipher_text

def p_example_nested_method_call(password, count, data):
    return p_example_method_call(password, count, data)

def p_example5_nested_method_call(password, data):
    count = 999
    return p_example_nested_method_call(password, count, data)

def get_pbk(salt, count):
    return PBKDF2(g_password, salt, 16, count=count)

def decrypt_aes_ecb(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    cipher_text = cipher.decrypt(data)
    return cipher_text

if __name__ == '__main__':
    print("PyCrypto -> PBE1000 -> p_example5_nested_method_call:", decrypt_aes_ecb(get_pbk(g_salt, g_count_lower_1000),
                                                                                   p_example5_nested_method_call(g_password,
                                                                                                                 g_plaintext)) == g_plaintext)
