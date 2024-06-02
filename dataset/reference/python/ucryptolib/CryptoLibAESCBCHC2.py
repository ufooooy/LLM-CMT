from ucryptolib import aes, MODE_CBC

def p_example2_hard_coded2(key, data):
    cipher = aes(key, MODE_CBC, bytes("1234567812345678", "utf8"))
    cipher_text = cipher.encrypt(data)
    return cipher_text