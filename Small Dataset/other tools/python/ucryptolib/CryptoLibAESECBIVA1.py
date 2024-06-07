from ucryptolib import aes, MODE_ECB, MODE_CBC

g_mode1 = MODE_ECB
g_mode2 = 1

def p_example13_indirect_g_variable_access1(key, data):
    mode = g_mode1
    cipher = aes(key, mode)
    cipher_text = cipher.encrypt(data)
    return cipher_text