from ucryptolib import aes, MODE_CBC

def p_example4_local_variable2(key, data):
    iv = bytes("1234567812345678", "utf8")
    cipher = aes(key, MODE_CBC, iv)
    cipher_text = cipher.encrypt(data)
    return cipher_text

