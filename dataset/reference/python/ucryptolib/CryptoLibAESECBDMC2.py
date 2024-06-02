from ucryptolib import aes, MODE_ECB, MODE_CBC

def p_example_method_call(key, data, mode):
    cipher = aes(key, mode)
    cipher_text = cipher.encrypt(data)
    return cipher_text

def p_example8_direct_method_call2(key, data):
    mode = 1
    return p_example_method_call(key, data, mode)