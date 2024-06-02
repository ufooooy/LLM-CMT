from ucryptolib import aes, MODE_ECB, MODE_CBC

def p_example4_local_variable2(data):
    key = bytes("1234567812345678", "utf8")
    cipher = aes(key, MODE_ECB)
    cipher_text = cipher.encrypt(data)
    return cipher_text