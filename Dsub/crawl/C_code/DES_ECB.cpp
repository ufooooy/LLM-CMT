#include <stdio.h>
#pragma warning(disable:4996)
#include <openssl/des.h>

int main(int argc, char** argv)
{
    DES_cblock key;
    DES_random_key(&key);

    DES_key_schedule schedule;
    DES_set_key_checked(&key, &schedule);

    const_DES_cblock input = "DEStest";
    DES_cblock output;

    DES_ecb_encrypt(&input, &output, &schedule, DES_ENCRYPT);

    printf("ciphertext: ");
    int i;
    for (i = 0; i < sizeof(input); i++)
        printf("%02x", output[i]);
    printf("\n");


    DES_ecb_encrypt(&output, &input, &schedule, DES_DECRYPT);
    printf("cleartext:%s\n", input);

    return 0;
}