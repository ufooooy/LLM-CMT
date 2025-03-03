#include <openssl/md5.h>
#include <stdio.h>
#include <string.h>
#pragma warning(disable:4996)

int main() {
    char cleartext[100] = "MD5TEST";
    char md5;

    unsigned char MD5result[16] = { 0 };
    const char temp[33] = { 0 };

    MD5((const unsigned char*)cleartext, strlen(cleartext), MD5result);
    printf("MD5result:");
    for (int i = 0; i < MD5_DIGEST_LENGTH; i++) {
        printf("%02X", MD5result[i]);
    }
   
    return 0;
}

