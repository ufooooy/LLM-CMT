#include <openssl/md4.h>
#include <stdio.h>
#include <string.h>
#pragma warning(disable:4996)

int main() {
    char cleartext[100] = "MD4TEST";

    unsigned char MD4result[16] = { 0 };
    const char temp[33] = { 0 };

    MD4((const unsigned char*)cleartext, strlen(cleartext), MD4result);
    printf("MD4result:");
    for (int i = 0; i < MD4_DIGEST_LENGTH; i++) {
        printf("%02X", MD4result[i]);
    }

    return 0;
}

