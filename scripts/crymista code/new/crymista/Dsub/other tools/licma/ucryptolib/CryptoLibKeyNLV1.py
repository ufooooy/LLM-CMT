from ucryptolib import aes, MODE_ECB, MODE_CBC

def p_example5_nested_local_variable1(data):
    key1 = b"1234567812345678"
    key2 = key1
    key3 = key2

    cipher = aes(key3, MODE_ECB)
    cipher_text = cipher.encrypt(data)
    return cipher_text