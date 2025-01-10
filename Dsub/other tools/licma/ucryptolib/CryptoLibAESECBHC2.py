from ucryptolib import aes, MODE_ECB, MODE_CBC

def p_example2_hard_coded2(key, data):
    cipher = aes(key, 1)
    cipher_text = cipher.encrypt(data)
    return cipher_text