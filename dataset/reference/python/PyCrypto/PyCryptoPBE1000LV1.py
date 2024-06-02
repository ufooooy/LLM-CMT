from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

g_password = "12345678"
g_plaintext = b"abcdefghijklmnop"
g_count_lower_1000 = 999
g_salt = b"12345678"

def p_example2_local_variable(password, data):
    count = 999
    key = PBKDF2(password, b"12345678", 16, count=count)

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
    print("PyCrypto -> PBE1000 -> p_example2_local_variable:", decrypt_aes_ecb(get_pbk(g_salt, g_count_lower_1000),
                                                                               p_example2_local_variable(g_password,
                                                                                                  g_plaintext)) == g_plaintext)
