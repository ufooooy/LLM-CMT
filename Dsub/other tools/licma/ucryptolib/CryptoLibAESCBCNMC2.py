from ucryptolib import aes, MODE_CBC

def p_example_method_call(key, iv, data):
    cipher = aes(key, MODE_CBC, iv)
    cipher_text = cipher.encrypt(data)
    return cipher_text

def p_example_nested_method_call(key, iv, data):
    return p_example_method_call(key, iv, data)

def p_example10_nested_method_call2(key, data):
    iv = bytes("1234567812345678", "utf8")
    return p_example_nested_method_call(key, iv, data)