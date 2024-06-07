from ucryptolib import aes, MODE_CBC

def p_example3_local_variable1(key, data):
    iv = b"1234567812345678"
    cipher = aes(key, MODE_CBC, iv)
    cipher_text = cipher.encrypt(data)
    return cipher_text