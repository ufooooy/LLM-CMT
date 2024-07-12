from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

g_password = "12345678"
g_plaintext = b"abcdefghijklmnop"
g_count_equal_1000 = 1000
g_salt = b"12345678"
g_salt1 = b"12345678"
g_salt2 = bytes("12345678", "utf8")

def p_example14_indirect_g_variable_access2(password, data):
    salt = g_salt2
    key = PBKDF2(password, salt, 16, count=1000)

    cipher = AES.new(key, AES.MODE_ECB)
    cipher_text = cipher.encrypt(data)
    return cipher_text

def get_pbk(salt, count):
    return PBKDF2(g_password, salt, 16, count=count)

def decrypt_aes_ecb(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    cipher_text = cipher.decrypt(data)
    return cipher_text

if __name__ == '__main__':
    print("PyCrypto -> StaticSalt -> p_example14_indirect_g_variable_access2:", decrypt_aes_ecb(get_pbk(g_salt, g_count_equal_1000),
                                                                                                p_example14_indirect_g_variable_access2(g_password,
                                                                                                      g_plaintext)) == g_plaintext)
