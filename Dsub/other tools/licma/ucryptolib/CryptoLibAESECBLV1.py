from ucryptolib import aes, MODE_ECB, MODE_CBC

def p_example3_local_variable1(key, data):
    mode = MODE_ECB
    cipher = aes(key, mode)
    cipher_text = cipher.encrypt(data)
    return cipher_text