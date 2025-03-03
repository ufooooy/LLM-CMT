from ucryptolib import aes, MODE_ECB, MODE_CBC

def p_example1_hard_coded1(key, data):
    cipher = aes(key, MODE_ECB)
    cipher_text = cipher.encrypt(data)
    return cipher_text


