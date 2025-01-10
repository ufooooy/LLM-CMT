from ucryptolib import aes, MODE_CBC

def p_example_method_call(key, iv, data):
    cipher = aes(key, MODE_CBC, iv)
    cipher_text = cipher.encrypt(data)
    return cipher_text

def p_example_nested_method_call(key, iv, data):
    return p_example_method_call(key, iv, data)

def p_example9_nested_method_call1(key, data):
    iv = b"1234567812345678"
    return p_example_nested_method_call(key, iv, data)