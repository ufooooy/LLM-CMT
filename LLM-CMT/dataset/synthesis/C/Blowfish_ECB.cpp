#include <stdio.h>
#include <string.h>
#include <openssl/blowfish.h>
#pragma warning(disable:4996)

int main() {
    unsigned char key[1024] = "SecretKey";
    unsigned char plaintext[1024] = "Blowfish";
    unsigned char ciphertext[1024]=  "";
    unsigned char decryptedtext[1024] = "";

    BF_KEY bf_key;
    BF_set_key(&bf_key, strlen((char*)key), key);
    
    BF_ecb_encrypt(plaintext, ciphertext, &bf_key, BF_ENCRYPT);
    printf("Encrypted: %s\n", ciphertext);

    BF_ecb_encrypt(ciphertext, decryptedtext, &bf_key, BF_DECRYPT);
    decryptedtext[strlen((char*)plaintext)] = '\0';
    printf("Decrypted: %s\n", decryptedtext);

    return 0;
}


