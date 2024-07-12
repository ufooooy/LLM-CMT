from ucryptolib import aes, MODE_CBC

g_iv1 = b"1234567812345678"
g_iv2 = bytes("1234567812345678", "utf8")

def p_example14_indirect_g_variable_access2(key, data):
    iv = g_iv2
    cipher = aes(key, MODE_CBC, iv)
    cipher_text = cipher.encrypt(data)
    return cipher_text