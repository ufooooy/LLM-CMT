from ucryptolib import aes, MODE_ECB, MODE_CBC

def p_example2_hard_coded2(data):
    cipher = aes(bytes("1234567812345678", "utf8"), MODE_ECB)
    cipher_text = cipher.encrypt(data)
    return cipher_text