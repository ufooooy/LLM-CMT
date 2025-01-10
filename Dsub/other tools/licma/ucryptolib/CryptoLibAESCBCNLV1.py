from ucryptolib import aes, MODE_CBC

def p_example5_nested_local_variable1(key, data):
    iv1 = b"1234567812345678"
    iv2 = iv1
    iv3 = iv2

    cipher = aes(key, MODE_CBC, iv3)
    cipher_text = cipher.encrypt(data)
    return cipher_text