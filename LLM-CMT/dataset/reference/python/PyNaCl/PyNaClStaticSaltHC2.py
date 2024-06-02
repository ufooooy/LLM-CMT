from nacl.secret import SecretBox
from nacl.pwhash.argon2i import kdf

g_nonce = b"123456781234567812345678"  # 24 byte
g_key = b"12345678123456781234567812345678"
g_password = b"12345678123456781234567812345678"
g_plaintext = b"abcdefghijklmnop"
g_salt = b"1234567812345678"
nonce = b"123456781234567812345678"  # 24 byte

def p_example2_hard_coded2(password, data):
    key = kdf(32, password, bytes("1234567812345678", "utf8"))

    secret_box = SecretBox(key)
    cipher_text = secret_box.encrypt(data, nonce)
    return cipher_text
def get_pbk(salt):
    return kdf(32, g_password, salt)

def decrypt(key, data):
    secret_box = SecretBox(key)
    cipher_text = secret_box.decrypt(data, g_nonce)
    return cipher_text

if __name__ == '__main__':
    print("PyNaCl -> StaticSalt -> p_example2_hard_coded2:",
          decrypt(get_pbk(g_salt), p_example2_hard_coded2(g_password, g_plaintext)[24:]) == g_plaintext)
