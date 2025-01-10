#include <iostream>
#include <string>
#include <openssl/rc2.h>
#include <openssl/rand.h>
#pragma warning(disable:4996)

int main() {

    const unsigned char* message = (unsigned char*)"Hello,RC2!";
    const unsigned char* key = (unsigned char*)"0123456789abcde";
    unsigned char iv[8] = "1234567";

    RC2_KEY rc2_key;
    RC2_set_key(&rc2_key, 128, key,0);

    unsigned char encrypted_message[1024];
    RC2_cbc_encrypt(message, encrypted_message, strlen((char*)message), &rc2_key, iv, RC2_ENCRYPT);
    
    unsigned char decrypted_message[1024]; 
    unsigned char iv2[8] = "1234567";
    RC2_cbc_encrypt(encrypted_message, decrypted_message, sizeof(encrypted_message), &rc2_key, iv2, RC2_DECRYPT);

    printf("Decrypted: %s\n", decrypted_message);
    return 0;
}
