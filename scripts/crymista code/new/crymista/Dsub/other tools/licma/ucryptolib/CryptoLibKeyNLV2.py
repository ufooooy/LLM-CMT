from ucryptolib import aes, MODE_ECB, MODE_CBC

def p_example6_nested_local_variable2(data):
    key1 = bytes("1234567812345678", "utf8")
    key2 = key1
    key3 = key2

    cipher = aes(key3, MODE_ECB)
    cipher_text = cipher.encrypt(data)
    return cipher_text