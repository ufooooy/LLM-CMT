from ucryptolib import aes, MODE_CBC

def p_example1_hard_coded1(key, data):
    cipher = aes(key, MODE_CBC, b"1234567812345678")
    cipher_text = cipher.encrypt(data)
    return cipher_text