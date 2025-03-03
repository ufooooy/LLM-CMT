from ucryptolib import aes, MODE_ECB, MODE_CBC

def p_example1_hard_coded1(data):
    cipher = aes(b"1234567812345678", MODE_ECB)
    cipher_text = cipher.encrypt(data)
    return cipher_text