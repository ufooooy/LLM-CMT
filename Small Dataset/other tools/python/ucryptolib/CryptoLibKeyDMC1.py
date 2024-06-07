from ucryptolib import aes, MODE_ECB, MODE_CBC

def p_example_method_call(key, data):
    cipher = aes(key, MODE_ECB)
    cipher_text = cipher.encrypt(data)
    return cipher_text

def p_example7_direct_method_call1(data):
    key = b"1234567812345678"
    return p_example_method_call(key, data)