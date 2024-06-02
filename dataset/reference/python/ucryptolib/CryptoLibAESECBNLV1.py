from ucryptolib import aes, MODE_ECB, MODE_CBC

def p_example5_nested_local_variable1(key, data):
    mode1 = MODE_ECB
    mode2 = mode1
    mode3 = mode2

    cipher = aes(key, mode3)
    cipher_text = cipher.encrypt(data)
    return cipher_text