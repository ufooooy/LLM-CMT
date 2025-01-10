from ucryptolib import aes, MODE_ECB, MODE_CBC

def p_example4_local_variable2(key, data):
    mode = 1
    cipher = aes(key, mode)
    cipher_text = cipher.encrypt(data)
    return cipher_text