from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

g_password = "12345678"
g_plaintext = b"abcdefghijklmnop"
g_count_equal_1000 = 1000
g_salt = b"12345678"

def p_example2_hard_coded2(password, data):
    key = PBKDF2(password, bytes("12345678", "utf8"), 16, count=1000)

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
    print("PyCrypto -> StaticSalt -> p_example2_hard_coded2:", decrypt_aes_ecb(get_pbk(g_salt, g_count_equal_1000),
                                                                               p_example2_hard_coded2(g_password,
                                                                                                      g_plaintext)) == g_plaintext)
