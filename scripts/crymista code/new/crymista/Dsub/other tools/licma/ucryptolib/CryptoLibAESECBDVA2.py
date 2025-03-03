from ucryptolib import aes, MODE_ECB, MODE_CBC

g_mode1 = MODE_ECB
g_mode2 = 1

def p_example12_direct_g_variable_access2(key, data):
    cipher = aes(key, g_mode2)
    cipher_text = cipher.encrypt(data)
    return cipher_text