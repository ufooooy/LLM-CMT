from ucryptolib import aes, MODE_ECB, MODE_CBC

g_key1 = b"1234567812345678"
g_key2 = bytes("1234567812345678", "utf8")

def p_example12_direct_g_variable_access2(data):
    cipher = aes(g_key2, MODE_ECB)
    cipher_text = cipher.encrypt(data)
    return cipher_text