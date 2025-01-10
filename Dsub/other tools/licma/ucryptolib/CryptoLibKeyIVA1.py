from ucryptolib import aes, MODE_ECB, MODE_CBC

g_key1 = b"1234567812345678"
g_key2 = bytes("1234567812345678", "utf8")

def p_example13_indirect_g_variable_access1(data):
    key = g_key1
    cipher = aes(key, MODE_ECB)
    cipher_text = cipher.encrypt(data)
    return cipher_text