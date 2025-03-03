from ucryptolib import aes, MODE_ECB, MODE_CBC

def p_example_method_call(key, data):
    cipher = aes(key, MODE_ECB)
    cipher_text = cipher.encrypt(data)
    return cipher_text

def p_example8_direct_method_call2(data):
    key = bytes("1234567812345678", "utf8")
    return p_example_method_call(key, data)