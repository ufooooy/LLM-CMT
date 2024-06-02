#include <stdio.h>
#include <openssl/rc2.h>
#pragma warning(disable:4996)

int main()
{
    const unsigned char* key = (unsigned char*)"0123456789abcdef";
    const unsigned char* input = (unsigned char*)"RC2_ECB";
    unsigned char encrypted[8];
    unsigned char decrypted[8];

    RC2_KEY rc2_key;
    RC2_set_key(&rc2_key, 128, key, 0);
    RC2_ecb_encrypt(input, encrypted, &rc2_key, RC2_ENCRYPT);
    printf("Encrypted: ");
    for (int i = 0; i < sizeof(encrypted); i++) {
        printf("%02x", encrypted[i]);
    }
    printf("\n");

    RC2_set_key(&rc2_key, 128, key, 0);
    RC2_ecb_encrypt(encrypted, decrypted, &rc2_key, RC2_DECRYPT);
    printf("Decrypted: %s\n", decrypted);

    return 0;
}